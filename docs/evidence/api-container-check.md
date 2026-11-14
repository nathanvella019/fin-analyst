# API and container checkpoint — 14 November 2026

## Verified

- Six unittest methods pass locally and inside Linux ARM64 (multiple validation/filter subcases).
- Real local API checks: Birner USD 63,843,837; Solera custom revenue USD 308,045,000; FutureFuel candidate USD 69,306,000 (known wrong, must refer); unsupported question; invalid February date (HTTP 422).
- All five actual HTTP responses from localhost:8008 match saved local API responses exactly, including SQL, provenance and flags. This is focused serving-consistency evidence, not a full 151-question served evaluation.
- Docker Compose reports healthy. Service runs as user `analyst`, with read-only prepared-data mount, two CPUs and 3 GB memory limit.
- Image `fin-analyst:rd1`: ID `sha256:fb15d86a5e70d697b7ae6a037ded61dfd32d94b7bc0b7ee56a3984892af7e198`; inspected size 1,203,599,174 bytes (1.20 GB decimal / 1.12 GiB); architecture arm64.
- Image uses the Dockerfile's pinned Python base digest and requirements. First build exposed a missing setuptools backend, resolved with explicit setuptools 80.9.0. Port 8000 was occupied; Compose uses host 8008 -> container 8000.

Detailed response evidence: ignored `data/evaluation/local_api_checks.json` and `docker_api_checks.json`. Repeat HTTP examples with `python3 scripts/check_api.py`. The script uses the notebook's known candidate values; it explicitly checks the referral decision even for the wrong candidate.

## Boundaries

All answers are review candidates, not approved automatic financial answers. FutureFuel still violates the release requirement. No external hosting, production approval, p95/load-test claim, dashboard, full fresh-clone retraining or CI gate is claimed. Initial logs include duration and question length, not a complete monitoring system. HTTP tests use sequential requests.

The six tests currently emit a Starlette notice that its HTTPX test backend is deprecated. They pass with pinned HTTPX 0.28.1. Migrating the testing backend can be done separately; it does not affect Uvicorn serving.

The image was built from the saved working tree before final documentation edits. Source changes are not committed yet. Rebuild after the eventual reviewed commit and record the resulting image ID with that commit for submission traceability.
