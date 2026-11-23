# RD2 Task 1 — Random company split and forward holdout

On 23 November 2026, two local MLflow runs fitted the supplied mapper at Git revision `6a1eac9`. A success means the expected standard tag appeared among five suggestions. Random selection used seed 3217 and held out 486 of 972 eligible companies. Both fits excluded the test companies from the vocabulary, search index and statement eligibility. Standard taxonomy metadata came from the permitted quarters.

| Fit | Training filings | Test cases | Correct / tested | Top-five accuracy | MLflow run ID |
|---|---|---|---:|---:|---|
| Random company split | 2016 Q1–Q4 | All held-out cases | 424 / 702 | 60.40% | `6f7618565ae94edea3d5b099c1562dde` |
| Same full-year fit | 2016 Q1–Q4 | Frozen Q2–Q4 cases | 200 / 345 | 57.97% | `6f7618565ae94edea3d5b099c1562dde` |
| Forward split | 2016 Q1 | Identical frozen Q2–Q4 cases | 201 / 345 | 58.26% | `7cdcc1f4615946c29634af72a9db2d67` |

The headline random score was 2.14 percentage points higher than the forward score. On the same cases the Q1 mapper got one more right overall. Ten cases succeeded only with the full-year fit and eleven only with the Q1 fit. The headline gap mixes a different test population with a different training window. These measurements give little basis for preferring one window on accuracy alone.

## What was frozen

The configuration records the start date of 1 April 2016, end date of 31 December 2016 and SHA-256 of the saved CSV. Its 345 cases comprise 190 from Q2, 85 from Q3 and 70 from Q4. The split uses the filing quarter in which a company/tag was first seen. Standard tags inferred from re-tagging are retrospective scoring references, and eligibility is based on companies for which such labels were found. RD1 had already examined this window. These choices limit claims about completely new companies or years.

The original file passed verification. Changing a quarter in an in-memory copy triggered a SHA-256 mismatch. The two completed MLflow runs carried the same frozen-file fingerprint. Counts were checked against their saved prediction files. All ten existing unit tests passed.

## Repeat locally

From the repository root with the four quarters prepared, install the tracking dependencies with `python -m pip install -r requirements-rd2.txt`. Run `python -m sec_analyst.rd2_splits score` to verify the saved holdout and repeat both fits. MLflow stores run records in `data/rd2-tracking/mlflow.db` and per-case predictions in its adjacent artifacts directory. A repeat creates new run IDs and updates the local results export. The Git checkpoint preserves this first comparison.

[Saved holdout](mapper-holdout-v1.csv) · [Run results and fingerprints](split-results.json) · [Nine design decisions](../../decisions/0011-rd2-mapper-holdout.md)
