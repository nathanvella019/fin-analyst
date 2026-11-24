"""Freeze and evaluate the Task 08 mapper splits from the repository root."""

import argparse
import hashlib
import io
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from sec_analyst.mapper import TagMapper
from sec_analyst.mapper_data import prepare_line_items, prepare_silver_labels
from sec_analyst.warehouse import connect_warehouse


COLUMNS = ["cik", "ctag", "label", "stmt", "fsq", "stag"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def csv_bytes(rows):
    return rows.to_csv(index=False, lineterminator="\n").encode("utf-8")


def verify(data, expected):
    actual = digest(data)
    if actual != expected:
        raise ValueError(f"Holdout SHA-256 mismatch: expected {expected}, got {actual}")


def split_cases(con, processed, settings):
    prepare_line_items(con, processed)
    silver = prepare_silver_labels(con, processed, settings["min_abs_usd"])
    companies = np.array(sorted(silver.cik.unique()))
    held = np.sort(np.random.default_rng(settings["seed"]).choice(
        companies, len(companies) // 2, replace=False
    ))
    cases = silver.loc[silver.cik.isin(held), COLUMNS].sort_values(["cik", "ctag"])
    if cases.duplicated(["cik", "ctag"]).any():
        raise ValueError("Duplicate company/tag test key")
    return held, cases.reset_index(drop=True)


def prepare_fit_inputs(con, processed, held):
    # Restrict the source view before the mapper fits its word vocabulary.
    con.register("held_companies", pd.DataFrame({"cik": held}))
    con.read_parquet(str(processed / "08_line_items.parquet")).create_view("all_lines")
    con.execute("""
        CREATE VIEW li AS
        SELECT l.* FROM all_lines l JOIN sub USING (adsh, cik, fsq)
        ANTI JOIN held_companies USING (cik) WHERE NOT l.custom
    """)
    # Hash the standard examples and the exact taxonomy labels used by this fit.
    pairs = con.sql("SELECT DISTINCT tag, label, stmt FROM li ORDER BY ALL").df()
    taxonomy = con.sql("""
        SELECT tag, any_value(tlabel) AS tlabel, 0 AS custom FROM tag
        WHERE custom=0 AND tag IN (SELECT tag FROM li)
        GROUP BY tag ORDER BY tag
    """).df()
    con.execute("DROP VIEW tag")
    con.register("tag", taxonomy)
    return digest(csv_bytes(pairs) + b'\x00' + csv_bytes(taxonomy))


def run_fit(settings, quarters, held, cases, later, mode, revision, experiment):
    import mlflow

    processed = Path(settings["processed_dir"])
    with mlflow.start_run(experiment_id=experiment, run_name=mode) as run:
        with connect_warehouse(processed, quarters) as con:
            training_hash = prepare_fit_inputs(con, processed, held)
            mlflow.set_tag("mlflow.source.git.commit", revision)
            mlflow.log_params({
                "git_commit": revision, "fit_quarters": ",".join(quarters),
                "holdout_start": settings["rd2"]["holdout_start"],
                "holdout_end": settings["rd2"]["holdout_end"], "seed": settings["seed"],
                "held_companies": len(held), "held_company_ids_sha256": digest(csv_bytes(pd.DataFrame({"cik": held}))),
                "training_inputs_sha256": training_hash, "holdout_sha256": digest(csv_bytes(later)),
                "test_sha256": digest(csv_bytes(cases)), "k": 5,
                "ngram_range": "1,2", "signals": "taxonomy,labels",
            })
            mapper = TagMapper(con)
        predictions, _ = mapper.suggest(cases)
        scores = cases.copy()
        scores["top5_correct"] = [target in tags for target, tags in zip(cases.stag, predictions)]
        scores["suggestions"] = [json.dumps(tags) for tags in predictions]
        subset = scores.merge(later, on=COLUMNS, validate="one_to_one")
        if len(subset) != len(later):
            raise ValueError("Shared scores do not cover the frozen holdout")
        results = {}
        for name, rows in [("shared", subset), ("test", scores)]:
            results[name + "_correct"] = int(rows.top5_correct.sum())
            results[name + "_count"] = len(rows)
            results[name + "_top5"] = float(rows.top5_correct.mean())
        mlflow.log_metrics(results)
        mlflow.log_text(csv_bytes(scores).decode(), "predictions.csv")
        return {"split": mode, "run_id": run.info.run_id, "commit": revision,
                "training_inputs_sha256": training_hash, **results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["freeze", "score"])
    parser.add_argument("--report", type=Path, help="Write fresh score results at this path")
    args = parser.parse_args()
    settings = yaml.safe_load(Path("config/config.yaml").read_text())
    cfg = settings["rd2"]
    processed = Path(settings["processed_dir"])
    path = Path(cfg["holdout_file"])
    if args.action == "score":
        frozen = path.read_bytes()
        verify(frozen, cfg["holdout_sha256"])
    with connect_warehouse(processed, settings["quarters"]) as con:
        windows = con.sql("SELECT fsq, min(filed) AS first, max(filed) AS last FROM sub GROUP BY fsq ORDER BY fsq").df()
        start, end = pd.Timestamp(cfg["holdout_start"]), pd.Timestamp(cfg["holdout_end"])
        early = windows.loc[windows["last"] < start, "fsq"].tolist()
        late = windows.loc[(windows["first"] >= start) & (windows["last"] <= end), "fsq"].tolist()
        if not early or not late or early + late != settings["quarters"]:
            raise ValueError("Configured dates must separate complete filing quarters")
        held, cases = split_cases(con, processed, settings)
    later = cases[cases.fsq.isin(late)].reset_index(drop=True)
    data = csv_bytes(later)
    if args.action == "freeze":
        if "holdout_sha256" in cfg:
            verify(data, cfg["holdout_sha256"])
        with path.open("xb") as file:
            file.write(data)
        print(len(cases), len(later), later.fsq.value_counts().to_dict(), digest(data))
        return
    verify(data, cfg["holdout_sha256"])
    later = pd.read_csv(io.BytesIO(frozen), keep_default_na=False)
    import mlflow
    tracking = Path("data/rd2-tracking").resolve()
    tracking.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(f"sqlite:///{tracking / 'mlflow.db'}")
    name = "RD2 Task 1 mapper splits"
    existing = mlflow.get_experiment_by_name(name)
    experiment = existing.experiment_id if existing else mlflow.create_experiment(
        name, artifact_location=(tracking / "artifacts").as_uri()
    )
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    results = []
    for mode, quarters, test in [("random-company", settings["quarters"], cases),
                                 ("forward-Q1", early, later)]:
        results.append(run_fit(settings, quarters, held, test, later, mode, revision, experiment))
    report = {"experiment_id": experiment, "holdout_sha256": digest(frozen), "runs": results}
    destination = args.report or path.parent / "split-results.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
