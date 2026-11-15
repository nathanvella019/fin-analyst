# Measuring response time and served-answer consistency

Run commands from the repository root with the API already healthy and the project virtual environment active.

```bash
python3 scripts/measure_api.py --label development
python3 scripts/measure_api.py --label held-out --phrasing held_out
python3 scripts/measure_api.py --label paced --requests 10 --rate-per-hour 150
```

The first two commands send all 151 reference questions, one at a time. They check that moving the answer code behind HTTP preserves its behavior. They are sequential functional sweeps with timing, not realistic sustained user traffic. The third sends ten questions at scheduled 24-second intervals, spanning approximately 216 seconds plus the last response. Its sample includes all six families. Use these runs separately; overlapping them interferes with the paced workload. Avoid sending extra questions through `/docs` during measurement.

The script reports p50 (half of requests finished within this time), p95 (95% finished within this time), HTTP status counts, client failures and candidate correctness. It records scheduling delay to expose a client that cannot keep up. Every request opens its own HTTP connection. Saved files are `data/evaluation/api_<label>/requests.csv` and `summary.json`. Running the same label overwrites that experiment's files; copy them elsewhere before repeating if you want to retain both runs.

The fixed set and random order are repeatable. Response times will vary with the Mac's load, Docker Desktop, file cache and question mix. These runs begin with the server already initialized; they do not measure startup or cold-cache performance. The paced sample has only ten requests, so its nearest-rank p95 is its slowest request. That is useful as an initial check, not a reliable estimate of rare slow responses.

150 questions/hour comes from the notebook's optional serving task S2. The economic policy uses 150 questions/week. One describes request arrival rate; the other scales modeled weekly costs. Do not confuse them.

The recorded correctness is for the **candidate** number. Every actual API decision remains referral for human review, including candidates that pass the notebook filter. HTTP 200 means the request was processed; the parser can still return `not understood` or `no rows`. Neither short response time nor HTTP success proves financial correctness.

The provisional demonstration budget is one second at p95. It is a stated design target, not an agreed production SLO. A longer realistic traffic experiment and user expectations are needed before making operational commitments. Compare full results and limitations in `docs/evidence/served-performance.md` and ADR 0005.
