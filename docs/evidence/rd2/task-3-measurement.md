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
