"""Run the notebook's five-rule-level answer evaluation and held-out wording."""

import argparse
from importlib.metadata import version
import json
from pathlib import Path
import sys
import time

import pandas as pd
import yaml

from sec_analyst.concepts import CONCEPTS
from sec_analyst.custom_map import prepare_custom_map
from sec_analyst.golden import build_golden_set, golden_fingerprint
from sec_analyst.mapper import ci95
from sec_analyst.mapper_data import prepare_line_items
from sec_analyst.service import RUNGS, QuestionService, correct
from sec_analyst.warehouse import connect_warehouse


def main() -> None:
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument(
        "--rebuild-golden",
        action="store_true",
        help="Replace the fixed reference questions using the configured data files",
    )
    args = arguments.parse_args()
    with Path("config/config.yaml").open(encoding="utf-8") as file:
        settings = yaml.safe_load(file)

    processed_dir = Path(settings["processed_dir"])
    output_dir = processed_dir.parent / "evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)
    golden_path = Path("tests/fixtures/golden_questions.parquet")
    manifest_path = golden_path.with_name("golden_manifest.json")

    with connect_warehouse(processed_dir, settings["quarters"]) as connection:
        started = time.perf_counter()
        if golden_path.exists() and not args.rebuild_golden:
            gold = pd.read_parquet(golden_path)
            fingerprint = golden_fingerprint(gold)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if fingerprint != manifest["gold_sha256"]:
                raise ValueError("Saved golden questions differ from their recorded fingerprint")
            print(f"Using fixed reference questions from {golden_path}", flush=True)
        else:
            gold, fingerprint = build_golden_set(
                connection, processed_dir, settings["quarters"],
                settings["seed"], settings["n_per_cell"],
            )
            golden_path.parent.mkdir(parents=True, exist_ok=True)
            gold.to_parquet(golden_path, index=False)
            manifest_path.write_text(json.dumps({
                "gold_sha256": fingerprint,
                "source_processed_dir": str(processed_dir),
                "quarters": settings["quarters"],
                "seed": settings["seed"],
                "n_per_cell": settings["n_per_cell"],
            }, indent=2) + "\n", encoding="utf-8")
        golden_seconds = time.perf_counter() - started
        print(f"Golden questions: {len(gold)}", flush=True)
        print(f"Families: {gold.groupby('family').size().to_dict()}", flush=True)
        print(f"Golden fingerprint: sha256:{fingerprint}", flush=True)

        started = time.perf_counter()
        prepare_line_items(connection, processed_dir)
        company_ciks = [int(cik) for cik in gold.cik.dropna().unique()]
        custom_map = prepare_custom_map(connection, company_ciks)
        mapping_seconds = time.perf_counter() - started
        print(f"Custom income-statement items mapped: {len(custom_map):,}", flush=True)
        revenue_members = custom_map.stag.isin(CONCEPTS["Revenue"][1]).sum()
        print(f"Mapped to revenue member tags: {revenue_members}", flush=True)

        service = QuestionService(connection)
        started = time.perf_counter()
        records = []
        for row in gold.itertuples():
            for rung, rung_name in enumerate(RUNGS):
                answer = service.answer(row.question, rung)
                records.append({
                    "i": row.Index,
                    "family": row.family,
                    "concept": row.concept,
                    "question": row.question,
                    "rung": rung_name,
                    "status": answer["status"],
                    "expected": row.answer,
                    "actual": answer["value"],
                    "correct": correct(answer["value"], row.answer),
                    "sql": answer["sql"],
                })
        runs = pd.DataFrame(records)
        development_seconds = time.perf_counter() - started
        ladder = runs.pivot_table(
            index="family", columns="rung", values="correct", aggfunc="mean"
        )[RUNGS]
        ladder.loc["all questions"] = runs.groupby("rung").correct.mean()[RUNGS]
        print(ladder.to_string(float_format="{:.1%}".format), flush=True)

        started = time.perf_counter()
        held_records = []
        for row in gold.itertuples():
            answer = service.answer(row.held_out, len(RUNGS) - 1)
            held_records.append({
                "i": row.Index,
                "family": row.family,
                "question": row.held_out,
                "status": answer["status"],
                "expected": row.answer,
                "actual": answer["value"],
                "correct": correct(answer["value"], row.answer),
                "sql": answer["sql"],
            })
        held = pd.DataFrame(held_records)
        held_seconds = time.perf_counter() - started
        final = runs[runs.rung == RUNGS[-1]]
        successes = int(final.correct.sum())
        lower, upper = ci95(successes, len(gold))
        profile = {}
        for name, results in [("development", final), ("held_out", held)]:
            profile[name] = {
                "correct": float(results.correct.mean()),
                "wrong_number": float(
                    ((results.status == "answered") & ~results.correct).mean()
                ),
                "refused_or_not_understood": float(
                    (results.status != "answered").mean()
                ),
            }
        metrics = {
            "gold_sha256": fingerprint,
            "gold_questions": len(gold),
            "development_checks": len(runs),
            "final_correct": successes,
            "final_accuracy": successes / len(gold),
            "final_accuracy_ci95": [float(lower), float(upper)],
            "phrasing_profile": profile,
            "held_out_failure_statuses": {
                status: int(count)
                for status, count in held[~held.correct].status.value_counts().items()
            },
            "configuration": settings,
            "python_version": sys.version,
            "package_versions": {
                package: version(package)
                for package in ("numpy", "pandas", "duckdb", "scikit-learn", "scipy", "pyarrow")
            },
            "timings_seconds": {
                "reference_preparation": golden_seconds,
                "custom_mapping_including_build": mapping_seconds,
                "development_evaluation": development_seconds,
                "held_out_evaluation": held_seconds,
            },
        }
        gold.to_parquet(output_dir / "golden_questions.parquet", index=False)
        runs.to_csv(output_dir / "development_answers.csv", index=False)
        held.to_csv(output_dir / "held_out_answers.csv", index=False)
        ladder.to_csv(output_dir / "accuracy_ladder.csv")
        (output_dir / "answer_metrics.json").write_text(
            json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Final development result: {successes}/{len(gold)} ({successes / len(gold):.1%})")
        print(f"95% interval: {lower:.1%}–{upper:.1%}")
        print(f"Held-out wording accuracy: {held.correct.mean():.1%}")
        print(f"Held-out failure statuses: {metrics['held_out_failure_statuses']}")
        print(f"Saved evaluation outputs under {output_dir}")


if __name__ == "__main__":
    main()
