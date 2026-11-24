"""Replay a proposed revenue referral rule on the frozen questions."""

import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import mlflow
import pandas as pd
import yaml

from sec_analyst.evaluate_policy import main as evaluate_policy
from sec_analyst.parser import QuestionParser
from sec_analyst.warehouse import connect_warehouse


def main():
    settings = yaml.safe_load(Path("config/config.yaml").read_text())
    processed = Path(settings["processed_dir"])
    tracking = (processed.parent / "rd2-tracking").resolve()
    tracking.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(f"sqlite:///{tracking / 'mlflow.db'}")
    name = "RD2 referral investigations"
    experiment = mlflow.get_experiment_by_name(name)
    experiment_id = experiment.experiment_id if experiment else mlflow.create_experiment(
        name, artifact_location=(tracking / "referral-artifacts").as_uri()
    )
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    with TemporaryDirectory() as folder, mlflow.start_run(
        experiment_id=experiment_id, run_name="revenue-review-replay"
    ) as run:
        output = Path(folder)
        evaluate_policy(output)
        answers = pd.read_csv(output / "policy_answers.csv")
        with connect_warehouse(processed, settings["quarters"]) as con:
            parser = QuestionParser(con)
            answers["parsed_concept"] = [parser.parse(q).get("concept") for q in answers.question]
        if answers.loc[answers.verified, "parsed_concept"].isna().any():
            raise ValueError("Verified answer missing its parsed concept")
        answers["with_revenue_review"] = answers.verified & ~answers.parsed_concept.eq("Revenue")
        fingerprint = json.loads((output / "policy_metrics.json").read_text())["gold_sha256"]
        mlflow.set_tag("mlflow.source.git.commit", revision)
        mlflow.log_params({"gold_sha256": fingerprint, "git_commit": revision,
                           "quarters": ",".join(settings["quarters"]), "review_concept": "Revenue"})
        for wording, group in answers.groupby("phrasing", sort=False):
            for rule in ("verified", "with_revenue_review"):
                accepted = group[rule]
                metrics = {"pass_filter": int(accepted.sum()), "refer": int((~accepted).sum()),
                           "wrong_passing": int((accepted & ~group.correct).sum())}
                mlflow.log_metrics({f"{wording}.{rule}.{k}": v for k, v in metrics.items()})
                print(wording, rule, metrics)
        mlflow.log_text(answers.to_csv(index=False), "replayed-questions.csv")
        print("MLflow run", run.info.run_id)


if __name__ == "__main__":
    main()
