# RD2 Task 2 — First local CI run

Run `make ci` from the repository root with the prepared four quarters and the dependencies in `requirements-rd2.txt`. Individual stages are `make lint`, `make test`, `make validate` and `make gate`. The combined command stops at the first failing stage.

Local implementation commit: `143cb1b`. Ruff passed, all ten unit tests passed, both frozen-set fingerprints matched and each of the four SEC tables contained the configured quarters. The gate recomputed predictions. The original Task 1 results export was preserved.

| Gate check | Result | Local rule |
|---|---:|---:|
| Correct original questions | 147/151 (97.35%) | At least 93.4% |
| Company-held-out mapper | 424/702 (60.40%) | At least 56.8% |
| Forward mapper on frozen cases | 201/345 (58.26%) | Provisionally reuse 56.8% until Task 3 |
| Wrong figures passing the notebook verification filter | 2 phrasings of one FutureFuel question | Zero |

The release gate returned status 1 and Make returned status 2. Both phrasings selected sales of goods ($69,306,000); the reference line excludes related-party sales ($66,893,000). Routing all answers to analyst review is a separate service policy.

Local mapper MLflow runs: random company `3b59c5211ab64f2eb15ef63119692867`, forward `9bf9b77ef82d455aaced7a0087b9cdb9`. Next: teach and agree the hosted workflow and data setup. The brief still requires links to passing and failing GitHub Actions runs. Task 3 will justify the metric and threshold using baseline and bootstrap evidence.
