# Using the monitoring dashboard

The dashboard tells us what the running program is doing. Open http://localhost:8008/monitor alongside http://localhost:8008/docs. Send a question in `/docs` and return to the dashboard. It updates every five seconds.

| Number | Meaning |
| --- | --- |
| Requests | Completed POST /ask requests since this process started |
| p95 response time | 95% of the latest 1,000 recorded requests completed within this time |
| Server errors | Requests ending with HTTP 500 or another 5xx code |
| Human referrals | Processed questions routed for review; currently expected for all candidates |
| Candidate status counts | Whether the given parser/model found an answer, found no rows or did not understand |
| Mean question characters | Average validated question length in the latest request window |
| Log write errors | Request metadata could not be saved; investigate if greater than zero |

A request can be processed successfully while returning no answer. That is different from a server crash. A financially wrong number can also arrive in an HTTP 200 response. We need reviewed answers to measure accuracy; the dashboard cannot discover that on its own.

Docker saves request metadata in its `request_logs` named volume at `/app/data/logs/requests.jsonl`. Each line is one JSON record. It contains lengths and statuses, not your question text. Local runs without Docker default to ignored `data/logs/`. Logs persist across ordinary Compose shutdown, while dashboard counts reset at startup. Avoid `docker compose down -v` if you want to keep the volume. Log rotation is not implemented yet.

The dashboard p95 is application-side elapsed time, not a realistic load-test result. A dedicated experiment must measure client-side timings, state the workload, show errors and count both answered and unsupported requests. Until that is done, do not use a handful of dashboard requests as a capacity claim.

After changing source code, `docker compose up --build -d --wait` rebuilds the image and restarts the process. Ordinary `up` reuses the old image. Rebuilding is why the previous dashboard counters disappear; persistent records remain.

## Separate client measurements

The full 151 development questions and 151 alternate phrasings were checked through HTTP on 15 November, matching offline values/statuses for all 302 responses. See [performance instructions](performance.md) and [measured evidence](evidence/served-performance.md). Client p95 is calculated separately from the mixed rolling dashboard window. A short paced sample at 150 questions/hour is the next rate check.
