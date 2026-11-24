# 0015 — Review input drift quarterly and require persistent accuracy loss before retraining

Proposed operating policy for RD2 Task 5, evaluated retrospectively on the four 2016 quarters.

| Decision | Rule | Why |
|---|---|---|
| Monitor a mapper input | After each filing quarter, compare the shares of custom lines on the five statement types with Q1. Use total variation, half the sum of the absolute share changes. | Statement type affects which tags the mapper can recommend. The shares can be measured as soon as filings arrive. |
| Alert the project owner | Review when the mix moves by at least 10%, or when quarterly top-five falls below the Task 3 floor of 52.66%. A quarter with missing scores needs a label check. Review new filers, unfamiliar tags, the taxonomy release and examples of misses. Re-evaluate on a new taxonomy release. | A 10% shift means one tenth of the mix would need reallocating to match Q1. Q2 moved 6.36% and scored 59.47%. Q3 crossed 10% while accuracy rose. This threshold prioritises inspection and was chosen using this replay. |
| Train a candidate | Trigger after two consecutive scored forward quarters below the floor. A missing quarter breaks the streak. Use the supplied training code, document the new training cutoff before scoring and evaluate on later cases. | Q4 alone scored 36/70. Its 95% interval spans 39.13–63.89%. A second low quarter gives more evidence of a persistent problem. Waiting can delay a response, so an individual low quarter already raises an alert. |
| Move the champion alias | For this individual project, Nathan owns promotion and rollback. Inspect the score and error examples, run the existing release checks and confirm that the previous version can be restored. The monitoring command only reports. | An input change can be harmless and a newly trained candidate can perform worse. Passing an alert threshold does not establish a benefit from replacing the model. |

Check the pooled labelled score each year because quarterly test sizes vary. A repeated label on the wrong line, a change in wording inside one statement type or a wrong financial answer further down the service may escape this input statistic. Keep the separate financial-answer gate and analyst review. This local replay is a monitoring plan, with no scheduled production alert delivery.

[Quarterly figure, counts and verification](../evidence/rd2/task-5.md)
