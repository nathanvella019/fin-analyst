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

Docker saves request metadata in its `request_logs` named volume at `/app/data/logs/requests.jsonl`. Each line is one JSON record. Since revision `7552b91` it contains candidate values, filing provenance, generated SQL and model identity as well as lengths/statuses; it omits raw question text. See [prediction audit](prediction-audit.md). Earlier records used the smaller metadata-only format. Local runs without Docker default to ignored `data/logs/`. Logs persist across ordinary Compose shutdown, while dashboard counts reset at startup. Avoid `docker compose down -v` if you want to keep the volume. Log rotation is not implemented yet.

The captured dashboard reports an application-side p95 of 146.1 ms across 362 requests. The separate busy-period experiment measures the time seen by the client.

After changing source code, `docker compose up --build -d --wait` rebuilds the image and restarts the process. Ordinary `up` reuses the old image. Rebuilding is why the previous dashboard counters disappear; persistent records remain.

## Separate client measurements

The full 151 development questions and 151 alternate phrasings were checked through HTTP on 15 November, matching offline values/statuses for all 302 responses. The final busy-period test sent 60 requests at an assumed 360 per hour. Client p95 was 181.4 ms and 58 candidates were correct. Two questions returned no rows. All 60 went to review. See the [final measurements and workload assumptions](evidence/rd1-service-results.md).
