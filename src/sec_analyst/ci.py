"""Local CI validation and release checks for Task 08."""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import yaml

from sec_analyst.evaluate_policy import main as evaluate_policy
from sec_analyst.golden import golden_fingerprint
from sec_analyst.rd2_splits import verify
from sec_analyst.warehouse import connect_warehouse


def validate(settings):
    cfg = settings["rd2"]
    verify(Path(cfg["holdout_file"]).read_bytes(), cfg["holdout_sha256"])
    fixture = Path("tests/fixtures/golden_questions.parquet")
    gold = pd.read_parquet(fixture)
    manifest = json.loads(fixture.with_name("golden_manifest.json").read_text())
    if golden_fingerprint(gold) != manifest["gold_sha256"]:
        raise ValueError("Golden question fingerprint mismatch")
    quarters = settings["quarters"]
    with connect_warehouse(Path(settings["processed_dir"]), quarters) as con:
        for table in ("sub", "num", "pre", "tag"):
            present = con.sql(f"SELECT DISTINCT fsq FROM {table}").fetchall()
            if {q for q, in present} != set(quarters):
                raise ValueError(f"{table}: prepared data differs from configured quarters")
    print(f"Validated both fingerprints and all four prepared tables for {len(quarters)} quarters.")


def gate(settings):
    # Use this invocation's scores, keeping the original Task 1 evidence intact.
    with TemporaryDirectory() as directory:
        work = Path(directory)
        report = work / "splits.json"
        subprocess.run([sys.executable, "-m", "sec_analyst.rd2_splits", "score",
                        "--report", str(report)], check=True)
        runs = {r["split"]: r for r in json.loads(report.read_text())["runs"]}
        evaluate_policy(work)
        answers = pd.read_csv(work / "policy_answers.csv")
        original = answers[answers.phrasing == "question"]
        wrong = answers[answers.verified & ~answers.correct]
        by_family = answers.assign(
            wrong_number=answers.answered & ~answers.correct,
            no_answer=~answers.answered,
            wrong_verified=answers.verified & ~answers.correct,
        ).groupby(["phrasing", "family"]).agg(
            cases=("correct", "size"),
            correct=("correct", "sum"),
            wrong_number=("wrong_number", "sum"),
            no_answer=("no_answer", "sum"),
            wrong_verified=("wrong_verified", "sum"),
        )
        print("Final answers by wording and question family (rates use all cases in each row):")
        print(by_family.assign(
            accuracy=(by_family.correct / by_family.cases).map("{:.1%}".format),
            wrong_rate=(by_family.wrong_number / by_family.cases).map("{:.1%}".format),
        ).to_string())
        checks = [
            ("Original final answers", original.correct.mean(), 0.934),
            ("Company-held-out mapper top five", runs["random-company"]["test_top5"], 0.568),
            ("Frozen forward mapper top five", runs["forward-Q1"]["shared_top5"],
             settings["rd2"]["forward_top5_floor"]),
        ]
        passed = True
        for name, value, floor in checks:
            ok = value >= floor
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {value:.2%} (floor {floor:.2%})")
            passed = passed and ok
        print(f"{'FAIL' if len(wrong) else 'PASS'}  Wrong verified answers: {len(wrong)} (allowed 0)")
        for row in wrong.itertuples():
            print(f"  {row.phrasing}: {row.question} | returned {row.service:g}, expected {row.golden:g}")
        return passed and wrong.empty


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("validate", "gate"))
    stage = parser.parse_args().stage
    settings = yaml.safe_load(Path("config/config.yaml").read_text())
    if stage == "validate":
        validate(settings)
    elif not gate(settings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
