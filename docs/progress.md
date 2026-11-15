# Progress and next steps

Updated 15 November 2026. Immediate target: RD1, due 23 November 2026.

## What works

- Configured loading into Parquet: 27,677 filings, 7,229 companies, 10,890,076 facts.
- DuckDB access, seven concepts and 24 ordered tags, five accounting checks.
- Given mapper: 32.5% top-1 and 60.5% top-5 on 702 tags from held-out companies.
- Parser, SQL answering and custom mappings packaged; final development accuracy 147/151 (97.4%), alternate wording 128/151 (84.8%).
- Fixed reference questions, fingerprint and evidence of row-order sensitivity. R0/R1 differences are documented; R2–R4 match the earlier run.
- Notebook referral evaluation reproduces the six policy results. FutureFuel still passes the filter incorrectly; the required no-wrong-verified-answer release criterion fails.

## RD1 estimate: about 70% ready

The grouped technical-evidence work is now assembled and verified for RD1, with stated limitations. This is a rough work-completion estimate, not a predicted mark. Architecture/comparison is now drafted for Nathan to review; governance and reflection/submission materials remain.

| Work area | RD1 position | Evidence |
| --- | --- | --- |
| Given package/config/commands and thin notebook | Complete for investigation | `notebooks/analyst_client.ipynb`; four code cells verified |
| Baseline and fit time | Recorded, including prose differences | Final service table; fresh mapper build 6.32s |
| Three card quirks plus extra | Counts/guards documented | `docs/evidence/data-quirks.md` |
| Forward-in-time check | Notebook diagnostic + stricter input sensitivity | `docs/evidence/forward-time.md`; retrospective limits stated |
| Fresh copy | Current revision 7552b91 passes declared final-baseline checks | `rd1-reproduction-manifest.json` |
| API/container and serving consistency | Full 302-case comparison matches | Image identity and size in final table |
| Versioned prediction audit/monitoring/load | 362 records reconciled; actual dashboard capture; 60-request scenario | `docs/evidence/rd1-service-results.md` |
| Architecture/alternative/daily cost | Draft assessment complete for Nathan to review | ADR 0008: diagram, comparison and daily workflow costs; IT cost unmeasured |
| EU AI Act reasoning | Pending | Current primary sources, tier/provider/deployer |
| Reflection/PDFs/slides/video | Pending | Nathan's reasoning, 400–600 words, 5–8 slides, <=5 min video |

## Whole required project estimate: about 35%

This is a coarse scope estimate. None of C1–C5 is fully complete yet. C1 has accounting checks and initial trap regression tests but needs fuller independent checks and convention decisions. C2 has most extraction/evaluation and fresh-clone baseline reproduction, but needs raw-data contracts. C3 now has baseline policy evidence but needs sensitivity, a larger reviewed set and a signed decision. C4 has a local review API and tested container but no automated CI accuracy gate. C5 has a local service dashboard/metrics, but no MLflow registration or taxonomy/mapper drift monitoring. E1–E4 and mandatory S1 have not been implemented. Optional stretches are excluded from this estimate.

## Alignment and limitations

The original notebook is unchanged and its model has not been tuned or replaced. Code lives in our own repository under `src/`. The Python name `sec_analyst` was chosen at Nathan's request; the task card literally specifies `src/fin_analyst/`, so this departure must be explicit in the submission and confirmed against marking expectations. Pinned dependencies and fresh isolated local-clone reproduction are demonstrated for `7552b91`; early-rung ordering differences remain documented. The monitoring/performance implementation checkpoint is committed as `7552b91`, which passed fresh-clone reproduction. Evaluation artifacts in `data/evaluation/` are ignored by Git; a compact evidence report should be versioned with the final code commit.

## Recommended next sequence

1. Read `docs/evidence/rd1-service-results.md` and `docs/technical-evidence-guide.md` together. Current evidence is tied to implementation 7552b91; final documentation lives in a later evidence commit.
2. Review the simple architecture/comparison in ADR 0008 and decide which reasoning Nathan agrees with.
3. Research current EU AI Act classification/responsibilities for the intended use.
4. Gather Nathan's own reflections, then prepare the written PDF, slides PDF and <=5-minute video. Check the updated `docs/rd1-checklist.md`.

Known FutureFuel error, early-rung ordering and notebook-prose/hash differences stay visible. The service remains review-only. Complete final-project raw contracts/full convention checks/CI/MLflow and later extensions separately; they do not block writing honest RD1 evidence now.
