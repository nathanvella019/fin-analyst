# 0012 — Set a minimum top-five score for the forward mapper

Nathan approved this decision on 24 November 2026.

The mapper suggests standard accounting tags for a company's own tag. We count a hit when the expected tag appears among the first five. We use top-five for the gate because the task card measures that ability and we can compare it with the supplied taxonomy-only baseline. We also report top-one because the service uses the first suggestion for custom income lines. On the same 345 cases, the combined mapper scored 201 hits in the first five and 115 in first place. Taxonomy alone scored 150 and 77 respectively.

We set the forward minimum at the lower end of the reference mapper's 95% interval. We proposed that rule before computing the interval. We sampled whole companies together because tags from one company can share wording. On this fixed set of 345 cases, **182 hits pass and 181 fail**. Configuration stores the measured endpoint in full precision (0.5266106442577031). CI displays 52.66%.

| Percentage | Decision it supports |
|---|---|
| 52.66% | Block a build if its forward top-five score falls below this floor. A build can lose 19 of the reference's 201 hits and still pass. This is a tolerance we chose, not a guarantee that such a loss is harmless. |
| 56.8% | Keep the task card's minimum for the separate, full-year company split of 702 cases. |
| 58.26% | Use the measured 201/345 as the reference for monitoring changes. Requiring all 201 hits in every run would give no tolerance for a lower score. |
| 60% | Would require 207/345. We have no separate requirement for this target, and the supplied forward reference falls six hits short. |

The answer service has separate release checks. On 151 frozen questions, original-wording accuracy must reach 93.4%. Across both phrasings, every wrong figure passing verification blocks release, whoever the company is. CI reports wrong numbers and missing answers by question family so that a passing mapper score cannot hide those problems.

[Measured intervals, commit and MLflow run](../evidence/rd2/task-3-measurement.md) · [Frozen holdout and company split](0011-rd2-mapper-holdout.md)
