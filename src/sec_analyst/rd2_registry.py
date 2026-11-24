"""Fit, register and exercise the RD2 mapper using the local MLflow store."""

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

import joblib
import mlflow
import pandas as pd
import yaml
from mlflow.models import infer_signature

from sec_analyst.mapper import TagMapper
from sec_analyst.rd2_splits import COLUMNS, csv_bytes, digest, prepare_fit_inputs, split_cases, verify
from sec_analyst.registered_mapper import FEATURES, RANKS, RegisteredMapper
from sec_analyst.warehouse import connect_warehouse


def ranking_hash(cases, predictions):
    ranked = cases[["cik", "ctag"]].copy()
    ranked["combined_rankings"] = [json.dumps(row) for row in predictions[RANKS].values.tolist()]
    return digest(csv_bytes(ranked))


def fit(settings, cases, window, repeat, tracking):
    cfg = settings["rd2"]
    cutoff = date.fromisoformat(cfg["registry"][window + "_end"])
    if not date(2016, 1, 1) <= cutoff < date.fromisoformat(cfg["holdout_start"]):
        raise ValueError("Training must finish before the frozen holdout starts")
    processed = Path(settings["processed_dir"])
    with connect_warehouse(processed, settings["quarters"]) as con:
        held, all_cases = split_cases(con, processed, settings)
        frozen = all_cases[all_cases.fsq.isin(cases.fsq.unique())]
        verify(csv_bytes(frozen[COLUMNS]), cfg["holdout_sha256"])

    client = mlflow.MlflowClient()
    name = "RD2 Task 4 mapper registry"
    experiment = client.get_experiment_by_name(name)
    eid = experiment.experiment_id if experiment else client.create_experiment(
        name, artifact_location=(tracking / "registry-artifacts").as_uri())
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    with mlflow.start_run(experiment_id=eid, run_name=window + ("-repeat" if repeat else "")) as run:
        mlflow.set_tag("mlflow.source.git.commit", revision)
        with connect_warehouse(processed, ["2016q1"]) as con:
            con.execute("DELETE FROM sub WHERE filed IS NULL OR filed > ? OR filed < DATE '2016-01-01'", [cutoff])
            if window == "february":
                # The dictionary is quarterly. Only use tag/version pairs actually
                # present in eligible filings by February's cutoff.
                con.register("excluded", pd.DataFrame({"cik": held}))
                con.execute("""
                    CREATE TEMP TABLE early_taxonomy AS SELECT t.* FROM tag t
                    SEMI JOIN (
                        SELECT p.tag, p.version FROM pre p JOIN sub s USING (adsh)
                        ANTI JOIN excluded e ON s.cik = e.cik
                    ) used USING (tag, version)
                """)
                con.execute("DROP VIEW tag")
                con.execute("CREATE VIEW tag AS SELECT * FROM early_taxonomy")
            inputs = prepare_fit_inputs(con, processed, held)
            n, first, last = con.execute("""
                SELECT count(DISTINCT l.adsh), min(s.filed), max(s.filed)
                FROM li l JOIN sub s USING (adsh)
            """).fetchone()
            mlflow.log_params({"git_commit": revision, "window": window, "cutoff": cutoff,
                               "first_filing": first, "last_filing": last, "training_filings": n,
                               "training_inputs_sha256": inputs, "holdout_sha256": cfg["holdout_sha256"],
                               "holdout_start": cfg["holdout_start"], "held_companies": len(held),
                               "held_company_ids_sha256": digest(csv_bytes(pd.DataFrame({"cik": held}))),
                               "seed": settings["seed"], "k": 5, "ngram_range": "1,2",
                               "signals": "taxonomy,labels", "repeat": repeat})
            mapper = TagMapper(con)
        ranked = RegisteredMapper(mapper).predict(cases[FEATURES])
        hits = ranked.eq(cases.stag, axis=0)
        fingerprint = ranking_hash(cases, ranked)
        if window == "march" and fingerprint != cfg["registry"]["reference_rankings_sha256"]:
            raise ValueError("March rankings differ from the saved Task 3 rankings")
        metrics = {"cases": len(cases), "top1_hits": int(hits.rank_1.sum()),
                   "top5_hits": int(hits.any(axis=1).sum()), "top1": hits.rank_1.mean(),
                   "top5": hits.any(axis=1).mean()}
        mlflow.log_metrics(metrics)
        mlflow.log_param("rankings_sha256", fingerprint)
        mlflow.log_text(csv_bytes(pd.concat([cases, ranked], axis=1)).decode(), "rankings.csv")
        with TemporaryDirectory() as temp:
            path = Path(temp) / "mapper.joblib"
            joblib.dump(mapper, path, compress=3)
            info = mlflow.pyfunc.log_model(
                name="mapper", loader_module="sec_analyst.registered_mapper", data_path=str(path),
                code_paths=["src/sec_analyst"], signature=infer_signature(cases[FEATURES], ranked),
                pip_requirements=[*Path("requirements.txt").read_text().splitlines(),
                                  f"mlflow-skinny=={mlflow.__version__}"])
        mlflow.set_tag("mapper_uri", info.model_uri)
        print(json.dumps({"run": run.info.run_id, "model": info.model_uri, **metrics}, indent=2))


def demo(settings, cases, run_ids):
    cfg = settings["rd2"]
    name = cfg["registry"]["name"]
    client = mlflow.MlflowClient()
    runs = [client.get_run(rid) for rid in run_ids]
    if len(set(run_ids)) != 3:
        raise ValueError("The demonstration requires three distinct fits")
    for run, window, repeat in zip(runs, ["february", "march", "march"], [False, False, True]):
        params = run.data.params
        if (run.info.status != "FINISHED" or params["window"] != window
                or params["repeat"].lower() != str(repeat).lower()
                or params["cutoff"] != cfg["registry"][window + "_end"]
                or params["holdout_sha256"] != cfg["holdout_sha256"]):
            raise ValueError(f"Unexpected run or holdout: {run.info.run_id}")
        loaded = mlflow.pyfunc.load_model(run.data.tags["mapper_uri"])
        if ranking_hash(cases, loaded.predict(cases[FEATURES])) != params["rankings_sha256"]:
            raise ValueError("Reloaded rankings differ from the fitted mapper")
        if run.data.metrics["top5"] < cfg["forward_top5_floor"]:
            raise ValueError(f"{window} is below the approved floor; cannot use as champion")
    for key in ("git_commit", "training_inputs_sha256", "rankings_sha256"):
        if runs[1].data.params[key] != runs[2].data.params[key]:
            raise ValueError(f"March rebuild differs on {key}")

    versions = []
    for run in runs[:2]:
        existing = client.search_model_versions(f"name='{name}' AND run_id='{run.info.run_id}'")
        if existing:
            version = existing[0]
        else:
            version = mlflow.register_model(run.data.tags["mapper_uri"], name)
        versions.append(int(version.version))
    old = client.get_registered_model(name).aliases.get("champion")
    if old is not None and int(old) not in versions:
        raise ValueError(f"Champion already points to unrelated version {old}")
    history = []
    try:
        for action, index in [("select", 1), ("roll back", 0), ("restore", 1)]:
            client.set_registered_model_alias(name, "champion", versions[index])
            selected = client.get_model_version_by_alias(name, "champion")
            model = mlflow.pyfunc.load_model(f"models:/{name}@champion")
            actual = ranking_hash(cases, model.predict(cases[FEATURES]))
            if int(selected.version) != versions[index] or actual != runs[index].data.params["rankings_sha256"]:
                raise ValueError("Alias or its ordered predictions differ from the expected version")
            history.append({"action": action, "version": selected.version, "rankings_sha256": actual})
    except Exception:
        if old is None:
            client.delete_registered_model_alias(name, "champion")
        else:
            client.set_registered_model_alias(name, "champion", old)
        raise
    evidence = {"registered_model": name, "holdout_sha256": cfg["holdout_sha256"],
                "runs": [{"id": r.info.run_id, "artifact": r.data.tags["mapper_uri"],
                          "parameters": r.data.params, "metrics": r.data.metrics} for r in runs],
                "alias_checks": history, "cases_checked_per_reload": len(cases)}
    client.log_dict(run_ids[1], evidence, "registry-demonstration.json")
    print(json.dumps(evidence, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    train = actions.add_parser("fit")
    train.add_argument("window", choices=("february", "march"))
    train.add_argument("--repeat", action="store_true")
    drill = actions.add_parser("demo")
    drill.add_argument("runs", nargs=3, metavar="RUN_ID")
    args = parser.parse_args()
    settings = yaml.safe_load(Path("config/config.yaml").read_text())
    cfg = settings["rd2"]
    path = Path(cfg["holdout_file"])
    verify(path.read_bytes(), cfg["holdout_sha256"])
    cases = pd.read_csv(path, keep_default_na=False)
    tracking = Path("data/rd2-tracking").resolve()
    tracking.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(f"sqlite:///{tracking / 'mlflow.db'}")
    if args.action == "fit":
        fit(settings, cases, args.window, args.repeat, tracking)
    else:
        demo(settings, cases, args.runs)


if __name__ == "__main__":
    main()
