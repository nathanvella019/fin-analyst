"""Measure mapper metrics on the frozen Task 1 forward cases."""

import argparse
import json
from pathlib import Path
import subprocess

import mlflow
import numpy as np
import pandas as pd
import yaml

from sec_analyst.mapper import TagMapper
from sec_analyst.rd2_splits import COLUMNS, csv_bytes, prepare_fit_inputs, split_cases, verify
from sec_analyst.warehouse import connect_warehouse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data"))
    args = parser.parse_args()
    settings = yaml.safe_load(Path("config/config.yaml").read_text())
    cfg = settings["rd2"]
    evidence = Path(cfg["holdout_file"]).parent
    path = Path(cfg["holdout_file"])
    verify(path.read_bytes(), cfg["holdout_sha256"])
    cases = pd.read_csv(path, keep_default_na=False)
    reference = next(run for run in json.loads((evidence / "split-results.json").read_text())["runs"]
                     if run["split"] == "forward-Q1")
    tracking = (args.data / "rd2-tracking").resolve()
    mlflow.set_tracking_uri(f"sqlite:///{tracking / 'mlflow.db'}")
    client = mlflow.MlflowClient()
    prior = client.get_run(reference["run_id"])
    saved = pd.read_csv(client.download_artifacts(reference["run_id"], "predictions.csv"), keep_default_na=False)
    joined = cases.merge(saved, on=COLUMNS, how="outer", indicator=True, validate="one_to_one")
    if not joined._merge.eq("both").all():
        raise ValueError("Task 1 predictions and holdout differ")
    cases = joined.sort_values(["cik", "ctag"]).reset_index(drop=True)
    processed = args.data / "processed"
    with connect_warehouse(processed, settings["quarters"]) as con:
        held, _ = split_cases(con, processed, settings)
    quarters = prior.data.params["fit_quarters"].split(",")
    seed = settings["seed"]
    draws = 10_000
    rev = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    experiment = client.get_experiment_by_name("RD2 Task 3 gate metrics")
    eid = experiment.experiment_id if experiment else client.create_experiment(
        "RD2 Task 3 gate metrics", artifact_location=(tracking / "task3-artifacts").as_uri())
    with mlflow.start_run(experiment_id=eid, run_name="paired-company-bootstrap") as run:
        with connect_warehouse(processed, quarters) as con:
            training_hash = prepare_fit_inputs(con, processed, held)
            if training_hash != reference["training_inputs_sha256"]:
                raise ValueError("Q1 fitting inputs differ from Task 1")
            mlflow.set_tag("mlflow.source.git.commit", rev)
            mlflow.log_params({**prior.data.params, "git_commit": rev, "source_run": reference["run_id"],
                               "bootstrap_draws": draws, "bootstrap_seed": seed,
                               "bootstrap_unit": "company", "variants": "combined,taxonomy-only"})
            mapper = TagMapper(con)
        hits = pd.DataFrame({"cik": cases.cik, "count": 1})
        for variant, signals in [("combined", ("taxonomy", "labels")), ("taxonomy", ("taxonomy",))]:
            rankings, _ = mapper.suggest(cases, use=signals)
            if variant == "combined" and rankings != cases.suggestions.map(json.loads).tolist():
                raise ValueError("Combined rankings differ from Task 1")
            for k in (1, 5):
                hits[f"{variant}_top{k}"] = [target in tags[:k] for target, tags in zip(cases.stag, rankings)]
            cases[variant + "_rankings"] = [json.dumps(tags) for tags in rankings]
        grouped = hits.groupby("cik").sum()
        sample = np.random.default_rng(seed).integers(len(grouped), size=(draws, len(grouped)))
        totals = grouped["count"].to_numpy()[sample].sum(axis=1)
        metrics = {}
        estimates = {}
        for key in grouped.columns.drop("count"):
            counts = grouped[key].to_numpy()
            estimates[key] = counts[sample].sum(axis=1) / totals
            low, high = np.quantile(estimates[key], [0.025, 0.975])
            metrics.update({key: float(counts.sum()/len(cases)), key+"_hits": int(counts.sum()),
                            key+"_lo": float(low), key+"_hi": float(high)})
        for k in (1, 5):
            gap = estimates[f"combined_top{k}"] - estimates[f"taxonomy_top{k}"]
            metrics[f"gain_top{k}_lo"], metrics[f"gain_top{k}_hi"] = map(float, np.quantile(gap, [0.025, 0.975]))
        metrics.update(test_cases=len(cases), companies=len(grouped))
        mlflow.log_metrics(metrics)
        mlflow.log_text(csv_bytes(cases).decode(), "checked-predictions.csv")
        result = {"run_id": run.info.run_id, "commit": rev, "source_run": reference["run_id"],
                  "holdout_sha256": cfg["holdout_sha256"], "training_inputs_sha256": training_hash,
                  "bootstrap_draws": draws, "seed": seed, "metrics": metrics}
        text = json.dumps(result, indent=2) + "\n"
        mlflow.log_text(text, "gate-metrics.json")
        (evidence / "gate-metrics.json").write_text(text)
        print(text)


if __name__ == "__main__":
    main()
