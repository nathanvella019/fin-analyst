# RD1 technical evidence index

The revised diary uses the [clean monitoring run](rd1-grafana.md), [notebook timing, denominators and cost calculations](rd1-review-calculations.json) and [recorded API exchange](rd1-recorded-demo.json). The earlier fresh-copy experiment remains the source for reproducing the final answer scores.

The [20 November Grafana run](rd1-grafana.md) records the follow-up check using the Session 4 monitoring tools, with its own timing results and screenshot.

Start with `rd1-service-results.md` for the final consolidated table and dashboard panel. Technical implementation is revision `7552b91`; final documentation may live in a later commit. Keep each result tied to its own tested commit/image rather than treating every historical run as the same experiment.

| Requirement | Evidence |
| --- | --- |
| Given model/package and fit time | `fresh-clone-reproduction.md`, `reproduction-manifest.json` |
| Thin notebook client | `notebook-client.md`, `../../notebooks/analyst_client.ipynb` |
| Three listed data quirks plus an extra | `data-quirks.md`, `rd1-data_checks.json`, tests in `../../tests/test_sql_traps.py` |
| Forward-quarter evaluation | `forward-time.md`, `rd1-temporal_mapper.csv`, `rd1-temporal_metrics.json` |
| Fresh-copy reproduction | `fresh-clone-reproduction.md`, `reproduction-manifest.json`; current revision reproduction noted in final table |
| Exact serving identity/image size | `rd1-image.json`, final service table and experiment manifest |
| Full offline/served consistency | Final service table; per-question files under ignored `data/evaluation/` |
| Versioned audit records | `../prediction-audit.md`, final request-ID reconciliation report |
| Monitoring panel | `rd1-dashboard.png` captured from the actual running browser; final table explains its request window |
| Realistic declared workload and p95 | Final service table and client experiment summaries; ADR 0007 states the assumptions |

Historical evidence is retained for traceability. `served-performance.md` and `api-latency.png` describe earlier runs; the final RD1 table must be used for current-image measurements. The known wrong verified FutureFuel answer and R0/R1 ordering differences are limitations, not evidence to omit. These files are technical evidence, not Nathan's completed reflection or submission PDFs.
