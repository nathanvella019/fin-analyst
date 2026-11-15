# ADR 0005: Measure served answers and client-side latency

Date: 15 November 2026. Status: experiment design accepted; operational release remains blocked.

## Workload and method

Use the fixed, SHA-256-checked 151-question fixture. A seeded shuffle (3217) makes the order repeatable. For the paced run, place the first shuffled example of each family first, followed by the remaining shuffled questions, so the short sample covers all six families. First run all development questions sequentially through HTTP, then all alternate phrasings. These are full served-answer checks and short sequential bursts, not a claim about a sustained arrival rate.

Then run ten development questions at 150 requests/hour: one arrival every 24 seconds, lasting approximately 216 seconds from first to last arrival plus the final response. The rate comes from optional serving task S2; it is distinct from Section 6's economic assumption of 150 questions/week. Do not interchange these units in the report. This is a short paced smoke test at the target rate, not completion of S2 or proof of long-term capacity. Larger justified traffic runs remain necessary for strong tail-latency claims.

Time each request on the client from request construction to reading/parsing its complete response. Include unsupported/refused cases and HTTP failures; report their counts separately from candidate correctness. Use the nearest-rank p50/p95. Under a paced workload dispatch independently of previous completion, with up to four client threads; record scheduling delay so client queueing is visible. Timeouts are 120 seconds. Each request opens its own HTTP connection.

The service is already initialized: mapper loading/startup is excluded. Data and OS caches are warm after prior checks and earlier questions; no cold-cache claim. The local experiment uses Docker Desktop Linux ARM64, a single Uvicorn worker, serialized DuckDB access, two CPU quota and 3 GB memory limit. Client and server share the same Mac. Background activity and Docker Desktop overhead affect results. The paced run follows the functional sweeps; avoid other deliberate /ask traffic during it.

## Evidence and interpretation

Save individual timings/statuses/reference comparisons, summary settings, base commit, dirty flag and golden fingerprint under ignored `data/evaluation/api_<label>/`. Record actual image identity in the compact versioned evidence report. Report this as measured working-tree evidence until code and final image are tied to a reviewed commit. Financial accuracy is evaluated on candidate values; all actual decisions remain human referral.

A provisional one-second p95 budget is a design target for the local interactive lookup demonstration, not a measured user requirement or guaranteed SLO. Compare measured results to it, then reconsider it using user expectations and realistic deployment traffic. The dashboard's rolling p95 and experiment p95 can differ because the dashboard combines requests from different experiments and omits HTTP network transit.
