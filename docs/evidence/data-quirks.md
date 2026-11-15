# RD1 data-quirk evidence — 15 November 2026

Remeasured with `python3 -m sec_analyst.data_checks` in image/revision `7552b91`. Queries: `src/sec_analyst/data_checks.py`. Exact counts, values and fingerprints: [rd1-data_checks.json](rd1-data_checks.json). These measurements verify the notebook warnings on the actual prepared files.

| Card/notebook warning | Measured finding | Consequence if missed | Protecting test/check |
| --- | --- | --- | --- |
| Different durations at one date | 11,365 10-Qs have multiple NetIncomeLoss durations at period end | A six-month amount may answer a quarter question | `test_filters_reject_wrong_contexts`: qtrs subcase rejects a synthetic wrong-duration value |
| Co-registrant vs main entity | 14,736 of 72,273 Assets facts have a co-registrant (20.4%) | A subsidiary figure may replace the main company's | Same test, coreg subcase rejects a synthetic subsidiary value |
| Incompatible currencies | Annual Revenues sum: 74,975,678,207,290 across units vs 8,522,984,023,857 USD-only (8.8x) | Mixed-unit sum is not a meaningful dollar total | Same test, uom subcase rejects a JPY value |
| Later comparative/amended filings | Apple's 2015-09-30 Assets: 290,479,000,000 in three 10-Qs, then 290,345,000,000 in its 10-K; 883 amendments and 674 originals marked later amended | A later figure may replace the intended reporting context | `test_original_period_end_excludes_later_comparative`; annual/amendment fixture |
| Fiscal vs calendar year | 467/6,382 10-K labels differ from period-end calendar year; 466/469 January–March ends use prior year | Calendar filtering misses the intended fiscal report | Fiscal-2015/March-2016 fixture finds the report at R3 but not R2 |
| Additional discovery: file order affects sampling and tied SQL | Earlier: ten sampled NetIncome questions changed despite equal sorted eligible rows. Fresh clone: R0 seven values/five correctness flags change; R1 eleven values/ten flags; R2–R4 unchanged | A seed or equal aggregate score alone does not prove reproduction | Fingerprint-checked fixed fixture; ADR 0001 and per-question fresh-copy comparison; early-rung instability remains disclosed |

Full test names are in `tests/test_sql_traps.py`. Run `python3 -m unittest discover -s tests -v`. The data counts show these problems exist; synthetic tests isolate their effects and fail if a protected filter is dropped. They do not prove all filings are correct. Complete raw contracts and independent convention coverage remain final-project work.
