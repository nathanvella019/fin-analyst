# RD1 written entry — working draft

**Status: AI-assisted first-person draft requested by Nathan. Personal reactions and conclusions are suggested wording, not confirmed statements of his views. Nathan must review and personalise them before submission.**

Reflection body: **455 words** including section headings and AI disclosure. Review notes, evidence material and references below are outside that count. This is not a final submission PDF.

## Reflection body

### Would I put this figure in a report?

FutureFuel’s quarterly sales made me pause. The question asked for one figure. The service returned $69,306,000. I could trace it to the filing. I could even run the query a second time and get the same answer. Yet the line used for our reference answer gave $66,893,000. The service had picked sales of goods. To decide which figure belonged in a report, someone still had to read what each line covered.

That example changed how I read our score. The supplied model answered 147 of 151 questions correctly. When the same questions were phrased differently, it got 128 right. I would want an analyst to know both figures before relying on the service.

### What the tests taught me

One detail I would have missed is how much a date leaves out. In 11,365 quarterly filings, the same end date appeared on profit figures covering different lengths of time. Both numbers can be genuine. If I ask for three months of profit and get six, checking the date again gets me nowhere. Our test puts both figures in one filing and makes the query pick the quarter.

Docker exposed a different assumption. The notebook ran on my Mac, where a packaging tool called setuptools was already there. The clean build failed when it tried to install the project. Once the build installed that tool explicitly, a fresh copy reproduced the final scores. A few early queries still picked different rows when two filing lines had equal priority. Now I know what to check when someone says a run was reproducible.

### Where I would keep an analyst involved

I would load the filings each quarter, answer questions as they arrive and give the analyst the proposed figure alongside its source. During our busy-period test, 95% of requests finished within 181.4 milliseconds. The dashboard could tell me how quickly the service responded. It would take a reviewer who understood the question to spot the problem with the sales line.

Using the desk’s assumptions, reviewing everything costs about €700 per working day. Releasing every available answer comes to €892 once mistakes and referrals are counted. I would try selective release only after verified answers pass review with zero errors, the upper estimate of the error rate at 95% confidence falls below 1%, and 95% of requests still finish within a second.

That decision also depends on who will use the answer. Looking up a company’s sales is one use. If a lender wanted to use the service to assess a person’s creditworthiness, I would revisit the risk classification before agreeing to that change.

AI helped with code, organising evidence and drafting this entry. The personal interpretation is still mine to review.

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
