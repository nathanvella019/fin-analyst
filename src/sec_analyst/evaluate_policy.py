"""Evaluate the notebook's three referral policies on the fixed questions."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from sec_analyst.custom_map import prepare_custom_map
from sec_analyst.golden import golden_fingerprint
from sec_analyst.mapper_data import prepare_line_items
from sec_analyst.policy import passes_filing_filter, policy, signals
from sec_analyst.service import RUNGS, QuestionService, correct
from sec_analyst.warehouse import connect_warehouse


def main(output_dir: Path | None = None) -> None:
    settings = yaml.safe_load(Path("config/config.yaml").read_text())
    fixture = Path("tests/fixtures/golden_questions.parquet")
    gold = pd.read_parquet(fixture)
    fingerprint = golden_fingerprint(gold)
    manifest = json.loads(fixture.with_name("golden_manifest.json").read_text())
    if fingerprint != manifest["gold_sha256"]:
        raise ValueError("Golden questions differ from their recorded fingerprint")

    processed = Path(settings["processed_dir"])
    output = output_dir or processed.parent / "evaluation"
    output.mkdir(parents=True, exist_ok=True)
    with connect_warehouse(processed, settings["quarters"]) as connection:
        prepare_line_items(connection, processed)
        prepare_custom_map(connection, [int(cik) for cik in gold.cik.dropna().unique()])
        service = QuestionService(connection)
        records = []
        for phrasing in ("question", "held_out"):
            for row in gold.itertuples():
                question = getattr(row, phrasing)
                answer = service.answer(question, len(RUNGS) - 1)
                flags = signals(service, question)
                records.append({
                    "phrasing": phrasing,
                    "family": row.family,
                    **flags,
                    "filing_verified": passes_filing_filter(
                        connection, service.parser.parse(question), answer, flags
                    ),
                    "correct": correct(answer["value"], row.answer),
                    "question": question,
                    "golden": row.answer,
                    "golden tag": row.answer_tag,
                    "service": answer["value"],
                    "service tag": (answer.get("provenance") or [None, None])[1],
                })

    operations = pd.DataFrame(records)
    operations["verified"] = (
        operations.answered & ~operations.via_mapper & operations.single_candidate
    )
    analyst_eur = (
        settings["analyst_min_per_question"] / 60
        * settings["analyst_cost_per_hour_eur"]
    )
    policies = []
    for phrasing, group in operations.groupby("phrasing", sort=False):
        group = group.reset_index(drop=True)
        for name, show in (
            ("analysts answer everything", pd.Series(False, index=group.index)),
            ("show every answer", group.answered),
            ("show verified answers, refer the rest", group.verified),
            ("require filing support for revenue", group.filing_verified),
        ):
            policies.append({
                "phrasing": phrasing,
                "policy": name,
                **policy(group, show, settings["questions_per_week"], analyst_eur,
                         settings["wrong_number_cost_eur"]),
            })

    results = pd.DataFrame(policies)
    break_even = analyst_eur / settings["wrong_number_cost_eur"]
    # This notebook calculation assumes a break-even rate strictly between 0 and 1.
    zero_error_sample = (
        int(np.ceil(np.log(0.05) / np.log(1 - break_even)))
        if 0 < break_even < 1 else None
    )
    wrong_verified = operations[operations.verified & ~operations.correct]
    wrong_filing_verified = operations[operations.filing_verified & ~operations.correct]
    metrics = {
        "gold_sha256": fingerprint,
        "configuration": settings,
        "analyst_eur_per_answer": analyst_eur,
        "break_even_wrong_rate": break_even,
        "shown_answers_required_if_zero_errors": zero_error_sample,
        "wrong_verified_answers": len(wrong_verified),
        "answers_with_restatement_flag": int((operations.answered & operations.restated).sum()),
        "answered": int(operations.answered.sum()),
        "notebook_filter_no_wrong_verified_answers": len(wrong_verified) == 0,
        "wrong_filing_verified_answers": len(wrong_filing_verified),
        "release_gate_no_wrong_verified_answer_passes": len(wrong_filing_verified) == 0,
        "cost_scope": "Notebook assumptions: analyst referrals and wrong numbers; excludes infrastructure costs.",
    }
    operations.to_csv(output / "policy_answers.csv", index=False)
    results.to_csv(output / "policy_comparison.csv", index=False)
    wrong_verified.to_csv(output / "wrong_verified_answers.csv", index=False)
    (output / "policy_metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(results.to_string(index=False, float_format="{:.4f}".format))
    print(f"Break-even wrong rate: {break_even:.2%}")
    print(f"Shown answers needed with zero errors: {zero_error_sample}")
    print(f"Wrong answers passing the notebook filter: {len(wrong_verified)}")
    print(f"Saved policy evidence under {output}")


if __name__ == "__main__":
    main()
