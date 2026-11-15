# ADR 0004: Local service monitoring

Date: 15 November 2026. Status: accepted for RD1 development.

## Decision

Add `/metrics` (JSON) and `/monitor` (an HTML dashboard polling every five seconds) inside the existing service. This gives a small local deployment visible operational evidence without introducing another database or service. It is an initial monitoring implementation, not completion of the C5 drift/MLflow requirements.

Count POST /ask requests, HTTP status, candidate status and referrals. Measure elapsed wall time through the application middleware, including input validation, thread-pool scheduling and database-lock waiting, excluding network transit and full response delivery. Dashboard p95 is the nearest-rank 95th percentile of the latest 1,000 completed requests. Counters cover the current process session; p95 does not measure the earlier startup/mapper build.

Record timestamps in UTC, package version, session, duration and validated question length as JSON Lines. Do not log raw question text or financial values in this metadata file. Invalid bodies rejected before the route have no recorded question length. Persist records in a Compose named volume, separate from the read-only prepared data. Normal `docker compose down` preserves that volume; `down -v` would delete it. Dashboard counters reset on process restart; persistent files are not replayed into them.

If a write fails, increment the dashboard's log-write-error counter and report the failure in server logs while allowing the answer request to finish. Startup requires a creatable log directory. Records currently have no automated rotation; review retention before sustained operation.

## Why these numbers matter

An unanswered question can still be HTTP 200: the service understood the request format but its parser found no supported question. A 422 rejects input; a 500 indicates server failure. Human referrals are currently expected for every processed question because serving is review-only. Neither HTTP success nor SQL verification establishes financial correctness. Measuring online accuracy requires independently reviewed labels. Realistic traffic and client-side latency measurement remain a separate experiment.

## Limits

Single process only, consistent with the existing single-worker deployment. This JSON `/metrics` is not a Prometheus scrape endpoint. Package version 0.1.0 identifies the package release; exact commit/image attribution must accompany experiments because working-tree edits share that version. The dashboard is localhost-only through Compose and has no external assets. No alert thresholds, data/taxonomy drift implementation or automatic retraining is introduced by this change.
