# RD2 Task 3 — Measuring the forward mapper gate

The Q1 mapper ranked five tags for each of the 345 frozen April–December cases from 278 held-out companies. The fitting-input and holdout fingerprints matched the Task 1 run. All five suggestions, including their order, matched every saved prediction. The comparison used the notebook’s taxonomy-only scoring option on the same fitted inputs. The combined option also uses other filers’ line labels.

| Scoring option | Correct first | Top-one (95% interval) | Correct in first five | Top-five (95% interval) |
|---|---:|---:|---:|---:|
| Taxonomy only | 77/345 | 22.32% (17.97–26.78%) | 150/345 | 43.48% (38.12–48.80%) |
| Combined reference mapper | 115/345 | 33.33% (28.36–38.55%) | 201/345 | 58.26% (52.66–63.77%) |

In 86 cases the expected tag ranked second through fifth. The combined option improved top-five by 14.78 percentage points over taxonomy alone. The paired 95% interval for that improvement was 10.26–19.43 percentage points. Each of 10,000 draws sampled 278 companies with replacement, kept every selected company's cases together and computed tag-level rates using the resulting number of cases as denominator. Both scoring options used identical draws (seed 3217). Intervals use the 2.5th and 97.5th percentiles. They describe variability across companies in this retrospective holdout, conditional on the fixed Q1 fit and inferred labels.

## Approved threshold

The forward top-five floor is 0.5266106442577031. On 345 cases this requires 182 hits. The provisional floor required 196. The full-year company split keeps its own 56.8% floor. [Decision and trade-offs](../../decisions/0012-forward-mapper-gate.md)

## Reproduce and trace

Measurement commit `084a78b`, MLflow run `704dd329ca6c47e1a2d2c58caeefeac5`, source run `7cdcc1f4615946c29634af72a9db2d67`. From the public worktree with the existing Task 1 data and MLflow store in the sibling project, run:

```bash
PYTHONPATH=src ../fin-analyst/.venv/bin/python -m sec_analyst.rd2_metrics --data ../fin-analyst/data
```

[Exact metrics and fingerprints](gate-metrics.json)

## Service results by question type

Local `make ci` on commit `a76813d` scored every question in both phrasings. Each row below gives counts in the order **correct / wrong number / no answer**. Each wording uses the same questions. The CI log also prints the rates with the number of questions in that row as the denominator.

| Question type | Questions per wording | Original | Reworded |
|---|---:|---:|---:|
| Value on a date | 48 | 48 / 0 / 0 | 48 / 0 / 0 |
| Fiscal year | 40 | 38 / 1 / 1 | 19 / 1 / 20 |
| Quarter | 27 | 25 / 1 / 1 | 25 / 1 / 1 |
| Count | 12 | 12 / 0 / 0 | 12 / 0 / 0 |
| Rank | 12 | 12 / 0 / 0 | 12 / 0 / 0 |
| Sum | 12 | 12 / 0 / 0 | 12 / 0 / 0 |
| All | 151 | 147 / 2 / 2 | 128 / 2 / 21 |

The saved reworded-answer evaluation gives more detail on the 21 unanswered cases. The parser did not understand 19 fiscal-year questions, including Pfenex’s net sales. Two understood questions found no matching rows, one about Echo Global Logistics and one about EQT GP Holdings. Across both phrasings Union Carbide returned $87 million against expected annual revenue of $5.842 billion and failed verification. FutureFuel returned $69.306 million against expected quarterly sales of $66.893 million and passed verification in both phrasings.

Lint, ten unit tests and data validation passed. The three score checks passed. The zero-wrong-verified rule stopped release. The scores describe the frozen benchmark.

## What if an analyst reviewed every revenue question?

We replayed every question against the supplied model and parser. The candidate policy starts with the notebook's filter, then refers any answer whose parsed concept is Revenue. The routing decision reads the same question and parser output available at request time. Reference answers are used to score outcomes.

| Wording (151 each) | Filter | Pass filter | Go to review | Wrong among those passing |
|---|---|---:|---:|---:|
| Original | Notebook | 126 | 25 | 1 |
| Original | Also refer revenue | 106 | 45 | 0 |
| Reworded | Notebook | 115 | 36 | 1 |
| Reworded | Also refer revenue | 98 | 53 | 0 |

For original wording the extra reviews include 19 correct figures and one wrong figure. For reworded questions they include 16 correct figures and one wrong figure. The same underlying questions were tested twice. This retrospective comparison followed inspection of the errors and cannot establish future performance. Both filters were simulated. The deployed API still refers every request. The pending decision is whether to investigate a more selective filing-based rule. C3 permits referral decisions, while C4 still requires the wrong-verified-answer gate. This experiment does not give Task 2 a passing Actions run.

To reproduce from the project root with the four prepared quarters, run `python scripts/compare_revenue_review.py` in the installed project environment. Commit `3cc27e1`, MLflow run `33dae08ac7fd4db0bae0b10e8e410341`. The run records the golden-set fingerprint and saves the results for each question.

## Release gate evidence

Commit `47056c7` uses the same filing check in the API and in CI. It keeps the original notebook filter in the report. The table shows **wrong figures / figures passing the filter**, with 151 questions per wording. All questions still go to an analyst in the running API.

| Filter | Original | Reworded |
|---|---:|---:|
| Notebook | 1 / 126 | 1 / 115 |
| Refer all revenue | 0 / 106 | 0 / 98 |
| Require support from the filed income statement | 0 / 122 | 0 / 111 |

Compared with the notebook filter, checking the filing sent four more figures per wording for review. One was wrong and three were correct. Zero errors in 111 accepted reworded cases gives a one-sided 95% upper error bound of 2.66%. The business target is below 1%. The two phrasings cover the same facts and cannot be pooled as independent observations.

| RD2 Task 3 hand-in item | Evidence |
|---|---|
| Chosen metric | Correct tag in first five suggestions. Combined mapper 201/345 (58.26%), company bootstrap 95% interval 52.66–63.77%. |
| Threshold | At least 182/345 on the frozen forward set. The full-year company benchmark retains its own 56.8% floor. |
| Simple baseline and alternative metric | Taxonomy alone scored 43.48% top-five. For first suggestion only, the combined mapper scored 33.33% and taxonomy alone scored 22.32%. |
| Release check | 12 tests passed locally. Original accuracy 147/151, full-year company top-five 424/702, forward top-five 201/345. Zero wrong figures passed the filing filter. |
| Trace | Threshold measurement MLflow run `704dd329ca6c47e1a2d2c58caeefeac5`. Local release-gate run `e45f61d3047d489b88a1f9af0de30ee6` logs the scores, both fingerprints, Git revision, mapper run IDs and question-level results. |
| GitHub Actions | [Earlier failing push](https://github.com/nathanvella019/fin-analyst/actions/runs/45456067938) · [Push with filing verification](https://github.com/nathanvella019/fin-analyst/actions/runs/45490395112) |

[Threshold ADR](../../decisions/0012-forward-mapper-gate.md) · [Filing check ADR](../../decisions/0013-check-the-filed-revenue-line.md)
