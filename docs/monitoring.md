# Using the monitoring dashboard

## Prometheus and Grafana

The API counts and times every `POST /ask`. Prometheus reads those totals and measurements every five seconds. Grafana queries Prometheus to draw the graphs. For example, when a request is referred, the API increases its counter by one. The next collection sees the new total, and the next dashboard refresh shows the rise.

From `fin-analyst`, start Docker Desktop and run:

```sh
docker compose --profile monitoring up --build -d --wait
```

1. Open [Prometheus targets](http://127.0.0.1:9090/targets). The `financial-analyst` target should show **UP** once the API is ready. Prometheus reads `/metrics/prometheus` every five seconds and keeps the time series in a Docker volume.
2. Open [Financial Analyst Service in Grafana](http://127.0.0.1:3000/d/financial-analyst). The project supplies the dashboard and its connection to Prometheus. The local dashboard opens with viewer access.
3. Send a question from the [API form](http://127.0.0.1:8008/docs), then wait for the next Grafana refresh. Requests and referrals go up. The p95 and question-length panels first receive a value after a request supplies the relevant data.

For the same 60-question workload used in the earlier RD1 run, activate the project virtual environment and run:

```sh
python3 scripts/measure_api.py --label grafana-peak --requests 60 --rate-per-hour 360
```

The run takes about ten minutes and saves its client timings in `data/evaluation/api_grafana-peak/`. Grafana graphs the API's rolling p95 over the most recent 1,000 requests. The client script measures the full round trip for its 60 requests. Each graph point in Grafana is a snapshot of the API measurements at the time Prometheus collected them. Start a new API session if you want the rolling p95 to cover only your test.

Stop the stack with `docker compose --profile monitoring down`. Logs, stored measurements and Grafana state persist in their Docker volumes. The two monitoring ports bind to the Mac's loopback address.

The [20 November run](evidence/rd1-grafana.md) includes the measured graph, timings and request results.

## Built-in dashboard

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
