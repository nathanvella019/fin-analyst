# Progress and next steps

Updated 14 November 2026. Immediate target: RD1, due 23 November 2026.

## What works

- Configured loading into Parquet: 27,677 filings, 7,229 companies, 10,890,076 facts.
- DuckDB access, seven concepts and 24 ordered tags, five accounting checks.
- Given mapper: 32.5% top-1 and 60.5% top-5 on 702 tags from held-out companies.
- Parser, SQL answering and custom mappings packaged; final development accuracy 147/151 (97.4%), alternate wording 128/151 (84.8%).
- Fixed reference questions, fingerprint and evidence of row-order sensitivity. R0/R1 differences are documented; R2–R4 match the earlier run.
- Notebook referral evaluation reproduces the six policy results. FutureFuel still passes the filter incorrectly; the required no-wrong-verified-answer release criterion fails.

## RD1 estimate: about 50% ready

This is a rough completion estimate, not a predicted mark or a measure of time spent. Ten equally weighted work areas below score about 48% in total (90 + 90 + 70 + 30 + 85 + 90 + 20, divided by ten). Technical preparation is substantially further ahead than submission readiness.

| Work area | Approximate completion | Remaining evidence |
| --- | ---: | --- |
| Package the given method and configure commands | 90% | Thin notebook client, finish tests and checkpoint commits |
| Baseline evaluation and traceable results | 90% | Commit traceability, consolidate baseline differences |
| Data quirks and one additional investigation | 70% | Initial trap tests and quirk table now saved; extend independent checks |
| Fresh-copy reproducibility | 30% | Clean Linux image built; fresh clone and full data/model reproduction pending |
| HTTP service and serving consistency | 85% | POST /ask works; five local/container matches; full served benchmark pending |
| Project container | 90% | Healthy localhost service, image size recorded; commit-linked rebuild pending |
| Monitoring and realistic load | 20% | Basic versioned request logs; dashboard and realistic load/p95 pending |
| Architecture and alternative comparison | 0% | Four layers and measured trade-offs |
| Governance reasoning | 0% | Source-backed classification and responsibilities |
| Written reflection, slides and video | 0% | Nathan's reflection, 400–600 words, 5–8 slides, <=5 min video |

## Whole required project estimate: about 30%

This is a coarse scope estimate. None of C1–C5 is fully complete yet. C1 has accounting checks and initial trap regression tests but needs fuller independent checks and convention decisions. C2 has most extraction/evaluation but needs raw-data contracts and fresh-clone reproduction. C3 now has baseline policy evidence but needs sensitivity, a larger reviewed set and a signed decision. C4 has a local review API and tested container but no automated CI accuracy gate. C5 has local metrics but no MLflow registration/dashboard. E1–E4 and mandatory S1 have not been implemented. Optional stretches are excluded from this estimate.

## Alignment and limitations

The original notebook is unchanged and its model has not been tuned or replaced. Code lives in our own repository under `src/`. The Python name `sec_analyst` was chosen at Nathan's request; the task card literally specifies `src/fin_analyst/`, so this departure must be explicit in the submission and confirmed against marking expectations. Dependencies are recorded, but a fresh isolated reproduction has not yet been demonstrated. Recent source files are saved locally and remain uncommitted. Evaluation artifacts in `data/evaluation/` are ignored by Git; a compact evidence report should be versioned with the final code commit.

## Recommended next sequence

1. Review the API/Docker learning guide and try a request at http://localhost:8008/docs. The container is running locally; `docker compose down` stops it.
2. Review and commit the saved work. Rebuild and record image ID against the reviewed commit.
3. Complete independent trap checks and fresh-copy reproduction; add monitoring/dashboard and a justified load test.
4. Use measured evidence for architecture/governance reasoning and Nathan's RD1 reflection, slides and video.

See [API/Docker guide](api-and-docker.md), [container evidence](evidence/api-container-check.md) and [data quirks](evidence/data-quirks.md). The API uses review-only mode because FutureFuel still passes the notebook filter incorrectly. The model has not been changed.
