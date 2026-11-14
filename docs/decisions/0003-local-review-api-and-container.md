# ADR 0003: Local review API and Docker deployment

Status: accepted for the teaching/demo environment; operational release blocked.

## Decisions

- FastAPI validates JSON questions; Uvicorn serves HTTP. `POST /ask` calls the existing R4 service. `GET /health` becomes available after database and mapper initialization. FastAPI lifespan closes the connection on shutdown.
- Build the existing mapper once at startup, then pass it into custom-map preparation. Its algorithm is unchanged. Serialize requests with a lock around the shared DuckDB connection and changing custom-map table. Clear cached SQL results when that table changes. One worker avoids duplicating large mapper state. This favors correctness and laptop memory over parallel throughput; load testing remains necessary.
- Return candidates, provenance, screening flags and SQL verification for review. All requests receive `decision: refer` and `answer: null` until the known wrong-verified-answer failure is resolved through an authorized operating decision. This is a serving restriction, not a change to the evaluated model. SQL is developer/reviewer evidence, not a proposed public end-user interface.
- Use Python 3.14.0 slim Linux pinned by image digest, pinned dependency versions, and setuptools 80.9.0 for package construction. Initial clean build failed without the build backend; explicitly installing it fixes that missing environment assumption.
- Mount prepared Parquet data read-only. Run data preparation first, including cached `08_line_items.parquet`; missing cache is a startup failure rather than silently downloading data in the API. The image excludes raw data, the virtual environment, Git history and secrets through an allowlist `.dockerignore`.
- Compose binds only localhost port 8008 (forwarded to container port 8000; host port 8000 was already occupied), with one non-root process, 3 GB memory and two CPUs. No external publication or cloud deployment. Logs contain version, answer status, decision, question length and timing, not the question itself. This is basic logging, not the required complete monitoring dashboard.

## Package naming departure

The task card specifies `src/fin_analyst/`. At Nathan's explicit request the internal Python package is `src/sec_analyst/`, while repository/distribution name remains `fin-analyst`. The src layout is preserved. Record this departure and confirm any literal naming requirement before submission.

## Limitations

No authentication or production deployment is claimed. API testing and image construction do not complete C1–C5. CI accuracy gates, raw-input contract, full independent convention tests, parent/subsidiary aggregation policy, reviewed operating policy, MLflow and dashboard remain outstanding. Dependency hashes and an image registry are not configured. Source changes remain uncommitted until Nathan reviews a checkpoint.
