"""Replay quarterly drift monitoring for the registered mapper."""

import argparse
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import mlflow
import numpy as np
import pandas as pd
import yaml

from sec_analyst.rd2_registry import ranking_hash
from sec_analyst.rd2_splits import COLUMNS, csv_bytes, digest, split_cases, verify
from sec_analyst.registered_mapper import FEATURES
from sec_analyst.warehouse import connect_warehouse

def mix_distance(counts, reference):
    """Total variation is half the sum of absolute differences in category shares."""
    totals = counts.sum(axis=1)
    if counts.isna().any().any() or (counts < 0).any().any() or (totals <= 0).any():
        raise ValueError("Each quarter needs valid, non-negative statement counts")
    # Subtract integer cross-products before dividing. An exact 10% shift
    # must still trigger an inclusive 10% threshold.
    differences = counts * totals.loc[reference] - np.outer(totals, counts.loc[reference])
    return differences.abs().sum(axis=1) / (2 * totals * totals.loc[reference])


def decisions(rows, reference, alert, floor, streak):
    """Rows are in calendar order; missing scores break a run of low quarters."""
    forward = rows.index > reference
    low = forward & rows.top5.lt(floor)
    return pd.DataFrame({
        "mix_alert": forward & rows.mix_distance.ge(alert),
        "accuracy_alert": low,
        "labels_missing": forward & rows.top5.isna(),
        "train_candidate": low.rolling(streak, min_periods=streak).sum().eq(streak),
    }, index=rows.index)


def company_interval(group, seed):
    totals = group.groupby("cik").hit.agg(["sum", "count"]).to_numpy()
    sample = np.random.default_rng(seed).integers(len(totals), size=(10000, len(totals)))
    hits, counts = totals[sample].sum(axis=1).T
    return np.quantile(hits / counts, [0.025, 0.975])


def plot(rows, alert, floor, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter

    fig, (mix, accuracy) = plt.subplots(2, 1, figsize=(8, 6.1), sharex=True, layout="constrained")
    x = np.arange(len(rows))
    mix.bar(x, rows.mix_distance, color="#32767a", width=0.45)
    mix.axhline(alert, linestyle="--", color="#89521a", label=f"Alert at {alert:.0%}")
    mix.set_ylim(0, max(0.15, rows.mix_distance.max() * 1.35))
    mix.set_ylabel("Share redistributed")
    mix.set_title("Change in custom statement-line mix from Q1", loc="left")
    for i, value in enumerate(rows.mix_distance):
        mix.annotate(f"{value:.1%}", (i, value), xytext=(0, 5),
                     textcoords="offset points", ha="center")
    mix.legend(loc="upper left", frameon=False)
    accuracy.errorbar(x, rows.top5, yerr=[rows.top5 - rows.low95, rows.high95 - rows.top5],
                      fmt="o-", capsize=5, color="#254f79", label="Top-five with 95% interval")
    accuracy.axhline(floor, linestyle="--", color="#89521a", label=f"Review below {floor:.2%}")
    accuracy.set_ylim(0, 1)
    accuracy.set_ylabel("Top-five accuracy")
    accuracy.set_title("Expected tag in the champion’s five suggestions", loc="left")
    accuracy.legend(loc="lower left", frameon=False)
    for i, row in enumerate(rows.itertuples()):
        accuracy.annotate(f"{row.hits}/{row.cases}", (i, row.high95), xytext=(0, 6),
                          textcoords="offset points", ha="center")
    labels = [q.upper().replace("2016", "") for q in rows.index]
    labels[0] += "\nreference"
    accuracy.set_xticks(x, labels)
    accuracy.set_xlabel("2016 filing quarter")
    for ax in (mix, accuracy):
        ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
        ax.spines[["right", "top"]].set_visible(False)
        ax.grid(axis="y", alpha=0.16)
        ax.set_axisbelow(True)
    fig.savefig(path, dpi=175)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/monitoring/rd2"))
    args = parser.parse_args()
    settings = yaml.safe_load(Path("config/config.yaml").read_text())
    cfg = settings["rd2"]
    policy = cfg["monitoring"]
    reference = policy["reference_quarter"]
    quarters = settings["quarters"]
    if quarters != [str(q).lower() for q in pd.period_range(reference, quarters[-1], freq="Q")]:
        raise ValueError("Use consecutive quarters starting with the reference")
    holdout = Path(cfg["holdout_file"])
    verify(holdout.read_bytes(), cfg["holdout_sha256"])
    frozen = pd.read_csv(holdout, keep_default_na=False)
    processed = Path(settings["processed_dir"])
    tracking = (processed.parent / "rd2-tracking").resolve()
    mlflow.set_tracking_uri(f"sqlite:///{tracking / 'mlflow.db'}")
    client = mlflow.MlflowClient()
    name = cfg["registry"]["name"]
    version = client.get_model_version_by_alias(name, "champion")
    fit_run = client.get_run(version.run_id)
    if fit_run.data.params["holdout_sha256"] != cfg["holdout_sha256"]:
        raise ValueError("Champion was evaluated on a different holdout")
    uri = f"models:/{name}/{version.version}"
    model = mlflow.pyfunc.load_model(uri)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    experiment_name = "RD2 Task 5 quarterly monitoring"
    experiment = client.get_experiment_by_name(experiment_name)
    eid = experiment.experiment_id if experiment else client.create_experiment(
        experiment_name, artifact_location=(tracking / "monitoring-artifacts").as_uri())
    with mlflow.start_run(experiment_id=eid, run_name="quarterly-champion-replay") as run:
        mlflow.set_tag("mlflow.source.git.commit", revision)
        with connect_warehouse(processed, quarters) as con:
            _, all_cases = split_cases(con, processed, settings)
            verify(csv_bytes(all_cases.loc[all_cases.fsq.gt(reference), COLUMNS]), cfg["holdout_sha256"])
            counts = con.sql("""
                SELECT fsq, stmt, count(*) AS n FROM li WHERE custom GROUP BY ALL
                ORDER BY fsq, stmt
            """).df().pivot(index="fsq", columns="stmt", values="n").fillna(0).reindex(quarters)
            context = con.sql("""
                WITH filers AS (
                    SELECT DISTINCT fsq, cik, min(fsq) OVER (PARTITION BY cik) AS first_q FROM sub
                ), names AS (
                    SELECT DISTINCT fsq, tag, min(fsq) OVER (PARTITION BY tag) AS first_q
                    FROM li WHERE custom
                )
                SELECT fsq, filers, new_filers, custom_names, new_custom_names FROM
                    (SELECT fsq, count(*) AS filers, count(*) FILTER (WHERE fsq=first_q) AS new_filers
                     FROM filers GROUP BY fsq)
                JOIN (SELECT fsq, count(*) AS custom_names,
                             count(*) FILTER (WHERE fsq=first_q) AS new_custom_names
                      FROM names GROUP BY fsq) USING (fsq) ORDER BY fsq
            """).df().set_index("fsq")
            taxonomy = con.sql("""
                SELECT fsq, version, count(*) AS facts FROM num
                WHERE NOT custom AND version LIKE 'us-gaap/%' GROUP BY ALL ORDER BY fsq, version
            """).df()
        tax = taxonomy.pivot(index="fsq", columns="version", values="facts").fillna(0)
        rows = context.reindex(quarters).copy()
        rows["custom_lines"] = counts.sum(axis=1)
        rows["mix_distance"] = mix_distance(counts, reference)
        rows["us_gaap_2016_share"] = tax["us-gaap/2016"] / tax.sum(axis=1)
        baseline = all_cases.loc[all_cases.fsq.eq(reference), COLUMNS]
        cases = pd.concat([baseline, frozen], ignore_index=True)
        ranked = model.predict(cases[FEATURES])
        forward = cases.fsq.gt(reference)
        if ranking_hash(cases.loc[forward], ranked.loc[forward]) != fit_run.data.params["rankings_sha256"]:
            raise ValueError("Forward rankings differ from the registered fit")
        cases["hit"] = ranked.eq(cases.stag, axis=0).any(axis=1)
        scores = cases.groupby("fsq").hit.agg(hits="sum", cases="size", top5="mean")
        rows = rows.join(scores)
        for q, group in cases.groupby("fsq"):
            rows.loc[q, ["low95", "high95"]] = company_interval(group, settings["seed"])
        alert = policy["statement_mix_alert"]
        floor = cfg["forward_top5_floor"]
        rows = rows.join(decisions(rows, reference, alert, floor, policy["quarters_below_floor_to_retrain"]))
        inputs_hash = digest(csv_bytes(counts.reset_index()) + b"\0" +
                             csv_bytes(context.reset_index()) + b"\0" + csv_bytes(taxonomy))
        params = {"git_commit": revision, "registered_model": name, "version": version.version,
                  "fit_run_id": version.run_id, "training_inputs_sha256": fit_run.data.params["training_inputs_sha256"],
                  "holdout_sha256": cfg["holdout_sha256"], "monitor_inputs_sha256": inputs_hash,
                  "reference_cases_sha256": digest(csv_bytes(baseline)), "accuracy_floor": floor,
                  "bootstrap_draws": 10000, "bootstrap_unit": "company", "seed": settings["seed"], **policy}
        mlflow.log_params(params)
        for step, (quarter, row) in enumerate(rows.iterrows(), start=1):
            mlflow.log_metrics({k: float(v) for k, v in row.dropna().items()}, step=step)
        with TemporaryDirectory() as temp:
            output = Path(temp)
            rows.to_csv(output / "quarterly.csv", index_label="fsq")
            counts.to_csv(output / "statement-counts.csv")
            taxonomy.to_csv(output / "taxonomy-counts.csv", index=False)
            plot(rows, alert, floor, output / "quarterly-monitoring.png")
            mlflow.log_text(csv_bytes(pd.concat([cases, ranked], axis=1)).decode(), "scored-cases.csv")
            manifest = {"run_id": run.info.run_id, **params,
                        "forward_hits": int(cases.loc[forward, "hit"].sum()), "forward_cases": int(forward.sum()),
                        "artifacts_sha256": {p.name: digest(p.read_bytes()) for p in sorted(output.iterdir())}}
            (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
            mlflow.log_artifacts(str(output))
            args.output.mkdir(parents=True, exist_ok=True)
            for file in output.iterdir():
                (args.output / file.name).write_bytes(file.read_bytes())
        print(rows[["mix_distance", "hits", "cases", "top5", "mix_alert", "accuracy_alert", "train_candidate"]])
        print("MLflow monitoring run", run.info.run_id)


if __name__ == "__main__":
    main()
