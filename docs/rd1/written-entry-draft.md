# RD1 written entry — working draft

**Status: AI-assisted first-person draft requested by Nathan. Personal reactions and conclusions are suggested wording, not confirmed statements of his views. Nathan must review and personalise them before submission.**

Reflection body: **498 words** by whitespace count. Review notes, evidence material and references below are outside that count. This is not a final submission PDF.

## Reflection body

For this investigation, I focused on turning the supplied financial statement notebook into a service that could be repeated and checked. I kept the given model unchanged and moved its code into a Python package. The final model answered 147 of 151 development questions correctly, but accuracy fell to 128 of 151 when the wording changed. This showed me that a strong result depends partly on how the questions are asked.

The most surprising result was that a wrong FutureFuel answer passed the notebook's verification filter. I had expected verification to mean the answer was correct. However, rerunning a query can confirm that a number came from the database without confirming that the chosen financial tag answers the intended question. This is why I would keep human review. A fast, successful response is useful, but it is not enough evidence to release a financial number automatically.

The data checks helped explain this problem. We found 11,365 quarterly reports containing more than one net-income duration at the same date. Without the correct duration filter, a six-month figure could answer a three-month question. Small tests made this easier to understand because they showed exactly what happened when a filter was removed.

Moving into Docker also exposed a missing packaging dependency. It worked in the existing environment but failed during the clean build until that dependency was included. A fresh copy then reproduced the final scores. Some early query results still changed with data ordering, which we documented. I learned that saving code and setting a random seed do not guarantee that every result will repeat.

The four architecture layers helped me connect these technical findings to the wider process. The business layer contains the analyst and the decision to use a number. The data layer contains filings and financial definitions. The application layer contains the package, API and dashboard. Docker and the Mac provide the technology layer. The dashboard can show slow requests or failures, but it cannot identify a financially wrong answer without reviewed reference answers.

Our service combines batch data preparation, online questions and human review. In the declared busy-period test, 95% of requests finished within 181.4 milliseconds. That met our provisional one-second budget. Using the notebook's assumptions, reviewing all questions costs about EUR 700 per working day, compared with EUR 892 for automatically releasing available answers and paying the assumed error and referral costs. These are estimates excluding shared IT costs; we have not measured any reduction in review time.

For the stated company-lookup purpose, the working AI Act assessment is non-high-risk, assuming the combined system qualifies as AI. Use in an individual's creditworthiness assessment would require reassessment. In a future deployment, the provider supplies the system under its name and the deployer uses it. I would reconsider automatic release only after stronger reviewed evidence meets the error threshold while keeping acceptable response times.

AI assistance supported the code, evidence organisation and this draft. The personal interpretation and final wording still require my own review before submission.

## Evidence to include with the final entry

- [Data-quirk table](../evidence/data-quirks.md).
- [Service-results table and actual dashboard panel](../evidence/rd1-service-results.md).
- [Four-layer diagram and pattern comparison](../decisions/0008-architecture-and-review.md).
- [Classification line and current official sources](../decisions/0009-ai-act-classification.md).

Measured implementation: `7552b91`; technical evidence: `b326794`. The body uses the final current-image p95 of 181.4 ms, not the earlier smoke-test figures. Known errors, original-notebook prose/hash differences and early-rung sensitivity remain documented in the evidence report. Cost figures are assumptions-based workflow estimates, not measured hosting bills or demonstrated savings.

## References for the classification paragraph

The non-high-risk conclusion is a working interpretation for the stated purpose, with AI-definition and deployment-scope qualifications. [Article 6](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6), [Annex III 5(b)](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3), [Article 3](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-3). The full note records prospective provider/deployer roles and the current local-development context. Do not describe this draft as a legal approval.

## Before submission

See [PENDING_FOR_NATHAN.txt](../../PENDING_FOR_NATHAN.txt). Confirm the claims about what surprised you and what you learned, decide whether you agree with the human-review recommendation and switch condition, and revise the AI disclosure to describe the review you actually performed. Do not remove the disclosure simply because the wording is edited. Recount the final body after edits and include the required evidence before exporting PDF.
