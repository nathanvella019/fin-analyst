# Financial Statement Analyst

[Run Prometheus and Grafana locally](docs/monitoring.md#prometheus-and-grafana). The same measurements that appear on the built-in dashboard are available as graphs over time in Grafana.

**Current RD1 files.** [Word report](output/RD1-entry-1.docx) · [Written PDF](output/pdf/RD1-entry-1.pdf) · [Seven slides](output/pdf/RD1-slides.pdf) · [Voice-over visuals](output/RD1-voiceover-visuals.mp4) · [Timed recording guide](output/RD1-recording-guide.txt). Clean monitoring code `4c9381e`, review evidence `cdce639`. Nathan’s personal sign-off and narration remain.

[Six-task review, 19 November](docs/rd1-checklist.md). All ten local tests passed. The written preview now shows three distinct numbered data traps and the extra row-order finding.

## RD1 written preview · 19 November 2026

[Open the four-page written preview](output/pdf/RD1-written-entry-preview.pdf). The 455-word reflection opens with the FutureFuel sales question and follows it through testing and the decision to keep human review. Nathan’s next step is to review the first-person reflection and AI disclosure before the final export, slides and video.

**START HERE: [Nathan's pending tasks](PENDING_FOR_NATHAN.txt) · [RD1 written draft](docs/rd1/written-entry-draft.md)**

Nathan requested that the personal reflection be filled in provisionally in a simple student tone and reviewed by him later. The draft is within 400–600 words and explicitly labelled AI-assisted/suggested first-person wording. Personal review remains pending; do not treat the draft as Nathan's confirmed reactions. The separate TXT file lists his review and submission tasks. No code or extra tests were added for this writing step.

## AI Act working assessment added — 15 November 2026

Added `docs/decisions/0009-ai-act-classification.md` using official current EU sources. Working conclusion: non-high-risk for the stated company-filings lookup, assuming the combined system qualifies as AI; Article 6/Annex III 5(b) and provider/deployer definitions are cited. The note distinguishes today's local development/testing from an enterprise deployment, flags the AI-definition boundary for a SQL/TF-IDF system, and raises the task's sole-trader/guarantor question for counsel. Direct-interaction transparency is noted under Article 50. Human review/disclaimers are not treated as automatic exemptions. Roles are conditional on who supplies the service under their name, not automatically assigned to the university/SEC/Docker. No code/infrastructure/tests changed. Nathan should review this reasoning before using it personally. Next: gather Nathan's own reflection, then write the 400–600 words and prepare slides/video.

## Simple architecture assessment added — 15 November 2026

Added one short document, `docs/decisions/0008-architecture-and-review.md`, containing the four-layer table/diagram, batch preparation + online answering + human review patterns, and a side-by-side comparison with automatic release of available answers. Used existing measured p95 (181.4 ms), observed held-out errors and notebook assumptions; no new tests or infrastructure. Assuming five working days, modelled review-all workflow cost is EUR 700/day vs automatic-release EUR 892/day (EUR 2,558 at its error upper bound), excluding shared unmeasured IT cost. Human review time/savings are not measured. Current review-all remains recommended because a wrong number passes the notebook filter; future switch requires the error gate, a demonstrated upper bound below 1%, and the provisional one-second latency budget. This is a working assessment for Nathan to review, not a claim that he personally approved every assumption or signed an enterprise decision. Next: current-source AI Act classification, then Nathan's reflection and submission materials. Keep explanations simple and do not add tests without a concrete need.

## RD1 technical evidence completed — 15 November 2026

Finished the technical-evidence scope requested by Nathan. Current implementation is committed as `7552b91`; final reports/documentation are recorded in the following evidence checkpoint. Start with `docs/evidence/rd1-service-results.md` in the repository for the single consolidated service table and actual dashboard panel, then `docs/technical-evidence-guide.md` for plain-language explanations.

Completed: thin notebook client (four code cells executed); real-data quirk queries/counts plus existing SQL regression guards; original quarterly mapper diagnostic plus separately time-restricted vocabulary/metadata refits; complete candidate audit with request UUID, value/provenance/generated SQL, flags, release decision and code/config/golden identity; exact serving-image metadata; final 302-case offline/served comparisons; stronger busy-desk workload; audit reconciliation; fresh local clone of current commit; actual Chrome dashboard screenshot and updated checklist.

Final serving image: sha256:0da6b54749409860753da57bdefa4bab150044d51a1ea9714546327058d52fd6, 1,203,903,312 bytes. Development 147/151 and alternate wording 128/151 still match all corresponding offline values/statuses/correctness. Client p95 141.5 ms / 125.4 ms respectively. Separate declared peak scenario: six analysts, one question per minute each; 60 scheduled requests at 360/hour over 590.11s. Client p50 116.5 ms, p95 181.4 ms, maximum 364.4 ms. All HTTP 200; 58 correct candidates and two no-row outcomes; all 60 referred. This is an assumed ten-minute busy-period scenario, not observed traffic or a production guarantee. Earlier 150/hour smoke-test and 150/week cost assumptions remain distinct.

All 362 unique request IDs reconciled with persisted audit values/statuses/identity/review decisions. Dashboard captured at 362 requests, 362 referrals, zero server/write errors; its mixed-window application p95 is 146.1 ms, not the workload-only client p95. Ten tests pass locally/in Linux. Fresh clone 7552b91 passed declared final-baseline checks; current mapper fitting/build 6.32s, scoring 1.18s. R2–R4 and held-out outputs match exactly; fresh R0 39.1% and R1 68.2% retain early-ordering differences. Raw hashes/image/stages are in `docs/evidence/rd1-reproduction-manifest.json`.

Measured quirks include 11,365 multi-duration reports; 14,736/72,273 co-registrant Assets facts (20.4%); 467/6,382 fiscal-year mismatches; 883 amendments; currency sums 75.0 trillion across incompatible units vs 8.5 trillion USD-only. Data/temporal outputs and compact per-request evidence are versioned under `docs/evidence/`; bulk data and full logs remain ignored. Audit format now includes public financial candidates/SQL, unlike the earlier metadata-only log; it still omits raw question text. The original notebook/model algorithm is unchanged. Notebook-prose top-1/hash/cost differences, retrospective temporal-benchmark limits and known FutureFuel error are explicitly retained in the final report.

RD1 technical checklist is checked off with limitations. Overall RD1 readiness is roughly 70% (not a mark); next are architecture/alternative-pattern and daily-cost reasoning, current-source AI Act classification, Nathan's reflection, then PDFs/slides/video. Complete final-project raw contracts, full convention tests, CI/MLflow, graph/LLM tasks later. Automatic financial release remains blocked. Main API remains running at localhost:8008; normal shutdown is `docker compose down`, which preserves the log volume. Avoid `down -v` if retaining audit records.

## RD1 technical evidence implementation — 15 November 2026

Added the thin notebook client, repeatable data-check queries, notebook-compatible quarterly mapper diagnostic and separate time-restricted input refits. Audit logs now include candidate value/provenance/generated SQL and code/config identity, with per-request IDs. Added build revision metadata and measurement-server identity capture. Ten tests pass; notebook code cells execute and reproduce Birner's value. Preliminary data/temporal measurements match the notebook diagnostic; final committed-image measurements and dashboard capture will be recorded after this implementation checkpoint. See ADR 0007. No model algorithm or supplied notebook changed.

## RD1 remaining-work checklist — 15 November 2026

Checked the original diary brief and local rubric against the saved implementation. The complete remaining-work checklist is [RD1 checklist](docs/rd1-checklist.md). It distinguishes required diary evidence from full-project tasks. Important open items: thin notebook client, final quirk table/traceability, forward-in-time evaluation evidence, complete versioned prediction audit, justified p95 workload and dashboard screenshot; architecture/cost comparison; current-source AI Act reasoning; Nathan's own reflection and three submission parts. Existing technical work is retained; no code/model changes were made for this checklist. Checklist/docs edits are not committed yet.

## Fresh-clone reproduction passed — 15 November 2026

Monitoring/performance implementation is committed as `f937aba` (`Add service monitoring and measured serving evidence`). Tested that exact full commit in a fresh local clone with a no-cache Linux image build and separate empty prepared-output folder. Four raw-file SHA-256 hashes/sizes and image identity are recorded. Runtime networking disabled; no existing processed caches copied. All ten tests passed; counts reproduced exactly (27,677 filings / 7,229 companies / 10,890,076 facts); mapper reproduced 32.5% top-1 / 60.5% top-5 on 702 tags. Final development 147/151 and alternate wording 128/151 reproduced. All R2–R4 per-question values/statuses/correctness and all held-out answers matched exactly; all six referral summaries matched.

Early-rule sensitivity remains: fresh R0 39.1% vs main 38.4%, with seven values/five correctness flags changed. R1 aggregate remains 69.5% but eleven values/ten correctness flags changed. These differences are consistent with the existing tied-row/order issue; they are not hidden or fixed by changing the model. The fixed benchmark fingerprint remains d9687a7d2ce416a9… . Known FutureFuel mistake still blocks automatic release.

Workflow: `docs/reproduction.md`, ADR 0006; compact evidence: `docs/evidence/fresh-clone-reproduction.md` and `reproduction-manifest.json` within the repo. Full logs/independent outputs: ignored `data/reproduction/f937aba-086oonfv/`. Build 110.59s; conversion 53.81s; mapper stage 14.83s; answer stage 16.77s; policy stage 13.53s. These are stage wall times, not API latencies. Main data and running Compose service were left untouched. Reproduction uses existing raw inputs; no claim about public remote-clone/download access or cross-architecture equality.

Approximate RD1 readiness now about 65%, full required project about 35%. Next: remaining independent data-convention checks and data contract, architecture comparison using measured evidence, current-source governance reasoning, and Nathan's own reflection/slides/video. This evidence/documentation checkpoint follows the tested code commit; final report should cite tested `f937aba` explicitly.

## Monitoring/performance Git checkpoint and next reproduction — 15 November 2026

Nathan asked to continue. Recording the monitoring/dashboard, persistent request metadata, full served-answer comparison, timing experiments, client tests and documentation in a local Git checkpoint. Added `scripts/reproduce.py` and `docs/reproduction.md` to repeat a fresh local clone/no-cache Linux build from a saved commit, with separate outputs and raw-file fingerprints. Execution of that fresh-copy workflow is pending at this checkpoint; results must be added after it finishes. Prior baseline and release limitations remain unchanged. No remote push is included.

## Served evaluation and timing checkpoint — 15 November 2026

Added `scripts/measure_api.py` with fingerprint verification, fixed-seed workload order, full development/alternate-wording HTTP sweeps and independently scheduled arrivals for a paced test. Per-request records and summaries save under ignored `data/evaluation/api_development/`, `api_held-out/` and `api_paced/`. New client tests prove wrong financial candidates are distinct from connection errors. All ten unit tests passed locally and inside the rebuilt Linux image.

The 151 development HTTP answers reproduced 147 correct; 151 alternate phrasings reproduced 128 correct. Every candidate value, status and correctness flag matched offline records across all 302 checks. All HTTP responses were 200 and all actual decisions remained referral. Sequential client p95: 137.0 ms development, 141.0 ms alternate wording. These are short warm functional sweeps, not sustained capacity measurements.

A separate ten-request sample, one arrival every 24 seconds (150/hour), covered all six question families over 216.08 seconds. All ten returned HTTP 200 and correct candidates; all were still referred. Client p50 115.4 ms; p95/maximum 779.6 ms; maximum dispatch delay 19.9 ms. With ten requests the nearest-rank p95 equals the maximum. This is a short smoke test at S2's target rate, not completion of S2 or a reliable long-term tail-latency claim. Section 6's 150 questions/week economic assumption is a different unit.

Documented provisional one-second p95 demonstration target and experiment limitations in ADR 0005. Measured image ID and resource limits are in `docs/evidence/served-performance.md`; timing chart `docs/evidence/api-latency.png`; repeat instructions `docs/performance.md`. Cold start, real analyst latency, electricity/hosting costs and prolonged/concurrent traffic remain unmeasured. Image packaging was then updated to include measurement scripts/tests. Dashboard counters reset during restart; persistent metadata remains in its named volume.

Both READMEs updated. Monitoring and experiment changes remain uncommitted on top of `ee3bfe5`; source/image attribution must be finalized before submission. Next: review/commit this checkpoint, complete independent convention tests and fresh-copy reproduction, then use measured evidence for architecture/governance and Nathan's RD1 reflection. Approximate RD1 readiness remains around 55–60%; whole required project about 30%. The model's known FutureFuel failure still blocks automatic release.

## Monitoring checkpoint — 15 November 2026

Nathan confirmed the restarted API worked. Added a local dashboard at http://localhost:8008/monitor, with JSON metrics at `/metrics`. It counts POST /ask requests, HTTP/candidate statuses, human referrals, server errors and metadata write errors. It measures application response time and validated question length; p95 uses the latest 1,000 completed requests. Dashboard polls every five seconds. These numbers describe service behavior, not financial correctness.

Metadata records contain UTC timestamps, package version, session ID, statuses, timing and question length, without question text or financial values. Docker persists them under `/app/data/logs/requests.jsonl` in the `request_logs` named volume. Ordinary `docker compose down` keeps the records; `down -v` deletes the volume. Live counters reset on restart. The metadata file currently has no automatic rotation.

Rebuilt/restarted the container successfully. All five existing HTTP checks still match the local API responses exactly. Observed counters: 5 requests, HTTP 200 x4 / 422 x1, three answered candidates, one unsupported question, four referrals, zero server errors/write errors. Five records persisted in the volume. This functional sample is not a realistic load test. Eight unit tests passed locally, including validation counts, server-failure recording, metadata privacy and restart behavior. See `docs/monitoring.md` and ADR 0004 in the repository.

Implementation is based on committed `ee3bfe5` with new uncommitted monitoring/docs changes. Next: Nathan opens `/monitor`, submits a question via `/docs`, and watches the count change. Then design and run a justified traffic experiment, report client-side p95/errors, and record evidence tied to the next reviewed commit/image. Approximate RD1 readiness is now about 55%; whole required project remains about 30%. Independent convention checks, fresh-copy reproduction and RD1 reasoning/submission work remain outstanding. No automatic financial release is enabled.

## Resuming — 15 November 2026

Verified implementation commit `ee3bfe5` on main and a clean working tree before updating these notes. Docker's engine socket was absent, so API availability has not been confirmed today. Nathan should open Docker Desktop, run `docker compose up -d --wait` from `fin-analyst`, then check `docker compose ps`. No data preparation or dependency reinstall is needed. Next teaching step: send the Birner question through `/docs` and understand candidate, provenance, signals and the review-only decision. After that, continue with monitoring/dashboard and measured response times for RD1, retaining the remaining independent-check/fresh-copy tasks. Progress estimates remain about 50% RD1 and 30% overall; restarting alone adds no completion. These new documentation edits are not yet committed.

## Git checkpoint — 14 November 2026

Nathan requested a local commit of the packaged baseline, fixed evaluation questions, referral evaluation, review-only API, Docker setup, tests and documentation. This checkpoint includes those files. The bulk dataset, virtual environment and `.env` files remain ignored. The small public-data golden-question fixture is intentionally versioned so evaluations use the same questions. The six tests passed locally and in the container during implementation; whitespace and staging checks were performed for this checkpoint. No remote push is part of this action.

Earlier entries below mentioning uncommitted work describe the state before this checkpoint. The parent `Project/README.md` is outside this Git repository and is saved separately. Use `git log -1 --oneline` to identify this checkpoint. The Docker image was built before final documentation changes; rebuild and record its resulting image ID when producing commit-linked submission evidence.

## End-of-day checkpoint — 14 November 2026

**Read this first when returning.** Nathan is stopping for today. The assistant has saved the project files and these notes. The service was last verified healthy at localhost:8008 in the previous work session. Nathan plans to stop it; shutdown has not been observed or performed by the assistant. Do not assume it is still running tomorrow.

### What Docker is doing

The image `fin-analyst:rd1` is the built package containing Linux, Python 3.14.0, pinned libraries and our program. The container is a running instance of that image. Docker Desktop supplies a managed Linux VM on this Mac; Nathan does not need to start his separate VM.

The container starts Uvicorn, the program listening for HTTP requests. FastAPI receives and validates questions. Startup opens DuckDB and builds the existing mapper in memory. While idle, the service waits for requests and keeps that memory available. It is not continually downloading SEC data, rerunning all evaluations or answering questions by itself. Docker periodically calls `/health` to check that the service responds.

Requests follow this route: browser or curl -> Mac port 8008 -> container port 8000 -> existing parser -> SQL -> DuckDB -> Parquet data -> JSON response. A port is a numbered connection point; the two ports are in separate environments. Host port 8000 was already occupied, so our project uses 8008. Compose only exposes this service on the Mac's localhost address, not as a public website.

The financial files remain under `data/processed/` on the Mac, attached read-only inside the container at `/app/data/processed/`. Docker did not copy the dataset into its image. DuckDB's temporary tables and mapper state live in memory and are recreated at the next start. Stopping the container does not delete the source code, prepared files, saved evaluation outputs or built image. The image consumes roughly 1.20 GB of disk space; Docker can also retain build cache. Running containers use memory/CPU; stopping this service releases its process resources, but Docker Desktop can still use resources until quit.

### Stop for today

Run in either the VS Code terminal or macOS Terminal:

```bash
cd "/Users/nathan/Documents/Uni/Year 3/Enterprise Business/Project/fin-analyst"
docker compose down
docker compose ps
```

`down` stops and removes this project's service container and Compose network. It keeps the image and the mounted Mac files. `ps` should list no running service rows afterwards. These commands do not need the Python virtual environment. Docker Desktop must still be running while issuing them. Afterward, quit Docker Desktop if desired; then close VS Code/the terminal or shut down the Mac. Transient container logs disappear with the container, but our saved check results remain on disk.

### Return next time

1. Open Docker Desktop and wait until its engine is ready.
2. Open the project in VS Code and run:

```bash
cd "/Users/nathan/Documents/Uni/Year 3/Enterprise Business/Project/fin-analyst"
docker compose up -d --wait
docker compose ps
```

`up` starts the service from the existing image; `-d` runs it in the background; `--wait` waits for its health check. Startup reloads the data access and mapper, so allow it to finish. Open http://localhost:8008/docs. There is no need to reinstall packages, reconvert the dataset or rebuild the image just because the computer was shut down.

If startup fails, inspect it with `docker compose logs --tail=50 api`. Do not delete data or reinstall everything. For a source/dependency change, rebuild with `docker compose up --build -d --wait`; ordinary `up` does not put edited source files into the existing image.

For Python development commands on the Mac, separately activate the existing environment:

```bash
source .venv/bin/activate
```

This activates the Mac's environment, not the container's Python. Docker commands do not require it.

### What is implemented and verified

- Original notebook method packaged in `src/sec_analyst/`; notebook itself unchanged.
- Four quarters prepared: 27,677 filings, 7,229 companies, 10,890,076 numeric facts.
- Fixed 151-question reference set: 147/151 development answers correct; 128/151 alternate wording correct. Earlier-rung row-order differences recorded.
- Baseline referral rules reproduced. Known FutureFuel mistake remains; both phrasings concern the same fact.
- FastAPI `POST /ask`, `GET /health`, interactive `/docs`; input validation, serialized database access, startup/shutdown cleanup and basic version/status/duration/question-length logging.
- Six unit-test methods pass locally and in the Linux image. Five actual HTTP responses match the local API responses exactly.
- Dockerfile, pinned base image/dependencies, Compose localhost mapping, non-root process and read-only data mount. Image size and ID recorded in the container evidence note.
- SQL tests demonstrate wrong-context rows entering when currency, co-registrant, quarter-duration or original-period filters are removed; annual fiscal-year/amendment fixture also checked. This is initial coverage, not all C1 requirements.

### Limits to remember

All API outputs remain **review-only**: `answer` is null, `decision` is refer, and `candidate` holds the model's proposed number and evidence. HTTP 200 means a request was processed, not that its financial answer is correct. No operational release, public deployment, full served benchmark, realistic load/p95 measurement, monitoring dashboard or finished RD1 submission is claimed.

Rough completion estimates: **RD1 about 50%; entire required project about 30%**. These are estimates of completed work, not expected marks. RD1 is due 23 November 2026.

### First work when we return

1. Let Nathan try the API and explain the response in his own words; continue teaching before adding more unfamiliar infrastructure.
2. Review `git status` and the saved changes, then make a deliberate Git checkpoint. The assistant has made no new commit. Uncommitted saved files survive shutdown but are not yet a Git snapshot or remote backup. Do not stage the ignored dataset or `.venv`.
3. Complete remaining independent data checks and fresh-copy reproduction. Build the monitoring dashboard and run a justified load test.
4. Record measurements against the reviewed commit/image, then prepare architecture comparison, governance reasoning and Nathan's own RD1 reflection/slides/video.

Detailed guides in the repository: `docs/api-and-docker.md`, `docs/progress.md`, `docs/evidence/api-container-check.md`, `docs/evidence/data-quirks.md`, and `docs/decisions/`. Detailed API check responses are saved under ignored `data/evaluation/`. Both this README and the parent Project README contain this checkpoint. Earlier progress entries below are chronological history.

ARI3217 Task 08 turns questions about SEC financial statements into answers with their filing sources. The immediate milestone is Reflective Diary Entry 1, due 23 November 2026.

## Current status

The loader, warehouse, concepts, mapper, parser, SQL answering and baseline evaluation are packaged in `src/sec_analyst/`. Final accuracy is 147/151 on development questions and 128/151 on alternate wording. The notebook referral policy is now evaluated too; FutureFuel still passes its filter incorrectly. A review-only POST /ask API now runs in Docker at localhost:8008. Six tests pass locally and in Linux; five HTTP responses match the local API exactly. Monitoring dashboard and load testing remain pending.

See [current progress and next steps](docs/progress.md) for the requirements review. Rough readiness estimates: RD1 about 50%, whole required project about 30%; these are completion estimates, not marks.

Nathan confirmed Docker Desktop works on the Apple silicon Mac by running `hello-world`. Reported versions are Docker 29.9.3 and Docker Compose v5.7.0.

The reference notebook is currently in the parent directory. The repository reads its prepared files from `data/processed/`; the parent notebook files remain available for comparison. Run the commands below from this repository root.

## Python environment

Use Python 3.14.0 and activate the project's virtual environment from the repository root.

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Nathan installed the notebook dependencies and reported successful dependency and import checks in the new environment. `requirements.txt` now records the installed dependency versions for fresh-copy reproduction.

The saved package configuration is in `pyproject.toml`. The Python package is named `sec_analyst`, referring to the SEC filings. Reinstall the editable project after the package rename and check the import.

```bash
python3 -m pip install -e .
python3 -c "import sec_analyst; print(sec_analyst.__file__)"
```

Nathan successfully installed `fin-analyst` version `0.1.0` in editable mode and confirmed that importing `sec_analyst` resolves to `src/sec_analyst/__init__.py`. The package setup is committed as `ec7fdc6`. The next implementation step is extracting the loader.

## Working folders

- `src/sec_analyst/` holds the Python code, imported as `sec_analyst`.
- `config/` holds project settings.
- `tests/` holds checks for the code and data rules.
- `notebooks/` holds notebook clients for the package.
- `docs/decisions/` holds short records of project decisions.
- `docs/diary/entry-1/` holds the first diary's evidence and submission materials.

Our collaboration notes and detailed progress are recorded in the parent `README.md`.

## Loader status

`src/sec_analyst/loader.py` contains `get_raw`, the notebook's streaming `unpack_members`, its exact `TSV` and `EXTRACT` settings, and `load_quarter` with explicit folder arguments. The queries preserve the notebook's column selection and exclusion of contact details. The VS Code KaggleHub import warning was resolved by selecting the project interpreter.

## Quarter conversion

On 14 November 2026, ran `load_quarter` using the project `.venv`, local raw file `../archive (1)/2016q1.json`, and output folder `data/processed/`. The conversion completed successfully:

| Table | Rows |
| --- | ---: |
| sub | 6,535 |
| num | 3,485,997 |
| pre | 1,051,814 |
| tag | 85,458 |

All four Parquet files were opened and counted with DuckDB. The numeric-fact count matches Nathan's notebook baseline. The `sub` column list matches the notebook selection. A repeat call skipped conversion because all four outputs existed. Git confirms the generated data file is ignored. Raw JSON was retained and the temporary directory was cleaned up automatically.

Both existing loader tests passed after adding the conversion function. The Kaggle download branch remains unverified because the raw file was available locally. Nathan subsequently ran Q2–Q4 successfully and reported full-year totals of 27,677 filings, 7,229 distinct companies and 10,890,076 numeric facts, matching the notebook baseline. These totals check dataset size, not every individual value. Next: review the loader changes and create a Git checkpoint, then continue packaging in small explained steps.

## Next guided step: configuration

Confirmed loader checkpoint `6672dc6` (`Extract and verify SEC data loader`) and a clean working tree before this step. Next Nathan will create `config/config.yaml`, as requested by the notebook, starting with the dataset handle, four quarters and local raw/processed paths. These paths initially resolve relative to the repository root. PyYAML is already pinned in `requirements.txt`; no new installation is needed for this step. Nathan created and saved `config/config.yaml`, then successfully read the dataset handle and four-quarter list with `yaml.safe_load`. Both raw and processed folder checks returned `True`. The remaining Section 0 model and evaluation settings will be migrated as their code is packaged.

`src/sec_analyst/prepare.py` now reads the YAML and calls `load_quarter` for each configured quarter. Run it from the repository root with `python3 -m sec_analyst.prepare`. Nathan reported the command worked as expected. PyYAML is declared as a direct dependency in `pyproject.toml`. Next refresh the editable installation metadata, run the existing tests and commit the configuration and command before adding the DuckDB connection code.

### DuckDB connection step

Configuration and preparation command committed as `410707f` (`Add configuration-driven data preparation`). Next Nathan creates `src/sec_analyst/warehouse.py` with `connect_warehouse(processed_dir, quarters)`. Preserve the notebook layout: materialise `sub` as a DuckDB table, expose `num`, `pre`, and `tag` as views over the explicitly selected quarterly files, and use a 1 GB memory limit and one thread. The assistant checked these relation operations against all four local quarters in a temporary in-memory connection and obtained 27,677 filings, 7,229 companies and 10,890,076 facts. Saving the module and running Nathan's import check remain pending.

### Warehouse module verified by Nathan

Nathan saved `src/sec_analyst/warehouse.py` and ran the import and connection check successfully. The available names were `num`, `pre`, `sub` and `tag`; totals were 27,677 filings, 7,229 companies and 10,890,076 numeric facts. The assistant inspected the saved module. Next guided step is extracting Section 3's exact `CONCEPTS` dictionary into `src/sec_analyst/concepts.py` and adding a function to create the notebook's `kb` table. Keep all phrases, tags and their precedence order. Concept-module creation and its 7-concept/24-member check are pending. Warehouse and concept work will need a Git checkpoint after review.

### Concept dictionary extracted and checked

At Nathan's request, copied the complete Section 3 `CONCEPTS` dictionary exactly into `src/sec_analyst/concepts.py`, below the existing imports, stopping before `kb_rows = []`. Added the supplied `register_concepts(connection)` function. An in-memory DuckDB check passed with 7 concepts and 24 member tags. All generated tags, priority positions and period types matched the dictionary; Assets produced `('Assets', 'Assets', 0, 'instant')`. Code and notes are saved locally. Next Nathan can repeat the check, then connect this knowledge table to the warehouse. Warehouse and concept changes still need a Git checkpoint after review.

### Next guided check: concepts with the warehouse

Next Nathan will open the configured warehouse, call `register_concepts` on that same connection, and join `kb` to standard tag definitions in `tag` to inspect member tags and official labels. This is a read-only check of the prepared files using an in-memory knowledge table. Nathan's integrated run is pending. After it passes, review and commit the warehouse and concept modules together.

### Concept and warehouse integration passed

Nathan ran the integrated check successfully. All seven preferred member tags joined to a standard tag definition: Assets, Cash, Equity, Liabilities, NetIncome, OperatingCashFlow and Revenue. This confirms the packaged warehouse and concept registration work together on one DuckDB connection. The query selected priority-zero members and one available taxonomy label per member. It does not evaluate question-answer accuracy. Next run the existing loader tests, review the staged warehouse and concept modules and README, and create a Git checkpoint. No commit has been made by the assistant.

### Accounting identity checks next

Confirmed warehouse and concepts commit `3794b2c` and clean working tree. Next Nathan creates `src/sec_analyst/checks.py` with the notebook's five `IDENTITIES` and `identity_check`, passing the DuckDB connection explicitly. Preserve source filters, context grouping, max-value selection, complete-row filtering and tolerance of the larger of USD 1,000 or 0.5% of the total. Module creation and running its five checks remain pending. Prior notebook results provide comparison targets of 99.96%, 84.19%, 95.64%, 94.98% and 82.65% in identity order.

### Accounting identity extraction and real-data checks passed

At Nathan's request, copied the notebook's complete `IDENTITIES` dictionary and `identity_check` function into `src/sec_analyst/checks.py`, stopping before the display code. Changed the function to receive `connection` explicitly and replaced its `con.execute` call with `connection.execute`. Ran all five checks through the configured warehouse. Counts and displayed percentages matched the prior notebook run: Assets/L&SE 24,895 and 99.96%; SalesRevenueNet/Goods+Services 1,107 and 84.19%; GrossProfit/Revenue-Cost 3,210 and 95.64%; ProfitLoss/NetIncome+NCI 7,292 and 94.98%; L&SE/Liabilities+StockholdersEquity 17,649 and 82.65%. All figures use the notebook tolerance and filters. The 10-K/10-Q form filter excludes /A forms but does not filter `prevrpt`; this preserves the notebook logic. Next review the results with Nathan and save the check module in Git. No new commit was made by the assistant.

### Next guided mapper preparation step

Next Nathan creates `src/sec_analyst/mapper_data.py` with `prepare_line_items(connection, processed_dir)`. It registers the notebook's label-normalisation SQL macro, prepares the exact Section 3 `line_items` query, caches the result as `08_line_items.parquet` and exposes `line_items` and `li` on the connection. This preserves the source cache behaviour for this stage. Creation and execution are pending. The custom company/tag count comparison target is 100,244. The accounting checks remain saved and verified, with their Git checkpoint still pending.

### Mapper line-item preparation passed

Nathan ran `prepare_line_items` through the configured warehouse and reported 100,244 distinct custom company/tag pairs, matching the notebook baseline. His five sample rows included repeated `AmortizationOfOverhaulCosts` rows with the cleaned label `amortization of overhaul costs` and statement `CF`, plus `AssetsNoncurrentExcludingPropertyPlantAndEquipment` with label `total other assets` and statement `BS`. The sample query displays filing/tag rows; the headline count uses distinct company/tag pairs. The assistant inspected the saved module. Next review and commit README, `checks.py` and `mapper_data.py`, then package the notebook's silver-label preparation. No new Git commit was made by the assistant.

### Silver-label preparation guided step

Confirmed accounting checks and line-item preparation committed as `b6195ba`, with a clean working tree. Next Nathan adds `min_abs_usd: 10000` to configuration and `prepare_silver_labels(connection, processed_dir, min_abs_usd)` to `mapper_data.py`, preserving the notebook's silver-label query, cached `08_silver.parquet` and final label/statement join. Expected outputs are 1,420 labelled custom company/tag pairs, 972 companies and 691 distinct standard targets. Creation and execution remain pending. These inferred labels provide the evaluation reference for the given mapper.

### Silver-label preparation executed and verified

At Nathan's request, added `min_abs_usd: 10000` to `config/config.yaml` and `prepare_silver_labels` plus its pandas import to `src/sec_analyst/mapper_data.py`. Copied the notebook's silver-label query and final label/statement join, reformatted the SQL for readability and passed the threshold, folder and connection explicitly. Ran the function against all four configured quarters. Results matched the notebook: 1,420 silver labels from 972 companies with 691 distinct standard targets. A second call reused the cache and returned the same data. Preparation and repeat checks took 5.5 seconds together, including warehouse and line-item setup. The formatted matching SQL was compared with the source and matched apart from whitespace and parameter substitution. Results are cached under ignored `data/processed/08_silver.parquet`. Code and both READMEs are saved locally. Next package the given mapper and its company split. This silver-label step has not been committed by the assistant.

### Given mapper packaged and evaluated

At Nathan's request, added `src/sec_analyst/mapper.py` with the notebook's CamelCase splitting, TF-IDF setup, two similarity signals, statement restrictions, suggestion ranking, three evaluation variants and Clopper–Pearson interval. Converted shared notebook variables into instance attributes and passed the warehouse connection explicitly. Added `src/sec_analyst/evaluate_mapper.py` as a runnable evaluation command and `seed: 3217` in configuration. Run from the repository root using `python3 -m sec_analyst.evaluate_mapper`.

The normal command completed successfully on all four quarters. Held out 486 of 972 labelled companies, with 702 test tags. Indexed 270,660 tag/label pairs and 6,067 candidate tags. Results matched Nathan's notebook run: taxonomy only 22.5% top-1 and 43.7% top-5; company labels only 22.2% and 50.9%; combined mapper 32.5% and 60.5%. Combined top-5 interval 56.8%–64.2%. Mapper construction took 8.34 seconds, including vocabulary fitting, vector transformation and company-filtered index construction; evaluation took 1.95 seconds. These timing boundaries differ from the notebook's narrower index timer. The notebook's all-company text vocabulary is preserved; the company split excludes held-out-company examples from the reference index and statement eligibility. This run reproduces the existing baseline methodology.

Code, configuration and both READMEs are saved locally. The silver-label and mapper changes remain uncommitted. Next inspect the packaged mapper results with Nathan and continue to the given question parser and SQL conventions in small explained steps. Full question-answer evaluation remains pending.

### Given question parser packaged and checked

Added `src/sec_analyst/parser.py` with the notebook's company-name cleaning, company lookup, question cleaning, date/fiscal-year extraction, raw-schema tag matching and query-intent rules. Company and schema lookup state now belongs to `QuestionParser`, created from an explicit warehouse connection. Kept the source phrase lists, matching order, refusals and raw-versus-concept behaviour. Expanded company/question cleaning into readable steps. Added `src/sec_analyst/parse_question.py` as a command. Example from the repository root: `python3 -m sec_analyst.parse_question "What were Dupont E I De Nemours's total assets at 31 December 2015?"`. Add `--raw` for the source raw-schema baseline.

The normal CLI run returned status ok, date 2015-12-31, CIK 30554, concept Assets, tag Assets and point intent. Inline compatibility checks compared 72 questions in both parser modes, for 144 comparisons against the original notebook functions, covering all six intents, familiar and held-out-style wording, unknown company/concept, ambiguous company and unrecognised input. All matched, including after the readability edits. Compared all 7,229 company-name normalisations to the original function, all matching. Company-name counts match the notebook: 7,229 companies, 7,204 normalised names and 24 names shared by multiple CIKs. Birner fiscal-2015 revenue and SIC 7389 fiscal-2015 loss count examples parsed as expected. These are compatibility checks, with full golden-set answer-accuracy evaluation still pending.

Code and both READMEs are saved locally. Silver-label, mapper and parser work is still awaiting a Git checkpoint. Next package SQL generation and execution plus the independent golden-answer path to evaluate complete answers. The parser command currently reports the interpretation of a question.

### SQL answer execution packaged and checked

Added `src/sec_analyst/service.py` with the notebook's `RUNGS`, SQL templates, cached SQL execution, answer statuses, numeric correctness tolerance and verification. `QuestionService` owns the warehouse connection and parser. Added `src/sec_analyst/ask.py` as a command, currently exposing rungs 0–3 and defaulting to rung 3, which includes the fiscal-year convention. Custom mapping (rung 4) still requires its mapping-table setup. Example from the repository root: `python3 -m sec_analyst.ask "What was Birner Dental Management Services's revenue in fiscal 2015?"`.

The normal command returned USD 63,843,837 from accession `0001140361-16-059508`, tag Revenues, period 2015-12-31, duration four quarters, 10-K filed 2016-03-30. Rerunning its SQL verified the same value. Compared 48 complete answers against the original notebook SQL functions across six question types, four rungs and both original-only settings. SQL, statuses, values and provenance matched. A deliberately incorrect claim failed verification, and unrecognised text returned the source refusal status. Full golden-set evaluation and R4 integration remain pending.

SQL teaching for Nathan covers SELECT as output columns, FROM as the starting table, JOIN as combining facts with filing details through adsh, WHERE as row filters, ORDER BY as selection order and LIMIT 1 as the first remaining row. The worked example uses company CIK 948072, Revenues, fiscal year 2015, annual 10-K, duration four quarters, filing-period date, parent reporting entity, USD and non-null value, ordered by filed date and accession. The actual service considers all concept member tags and applies tag precedence.

Code and both READMEs are saved locally. Recent mapper, parser and SQL changes still need a Git checkpoint. Next connect custom-tag suggestions and package the independent golden-answer evaluation path.

### Custom-tag mapper connected to the answer command

Added `src/sec_analyst/custom_map.py` with `prepare_custom_map(connection, company_ciks)`. It selects the requested companies' custom income-statement line items, uses the notebook's production mapper with every company's standard line items, takes the first suggestion and creates the expected in-memory `custom_map` table. Empty company lists and empty custom selections create an empty map without calling the mapper. Updated `ask.py` to expose rungs 0–4, default to rung 4, and prepare the selected company's map before answering a successfully parsed company question. Mapping scope follows the requested companies; the golden-set run will pass all golden companies together as the notebook does.

An integrated check reproduced the notebook's seven custom-revenue examples using its independent statement-label selection and compared all seven R4 answers with the original answer/SQL functions on the same mapping table. All matched. For this seven-question slice only, correct answers rose from 0/7 at R3 to 4/7 at R4. Mapped 167 custom income-statement items for these seven companies, suggesting 49 distinct standard targets. Solera quarterly revenue at 2015-12-31 changed from no rows to USD 308,045,000; Calpian fiscal-2015 revenue to USD 6,295,739; Oakridge fiscal-2015 revenue to USD 5,590,094; Bank of New York Mellon quarterly revenue at 2016-09-30 to USD 3,941,000,000. Remaining baseline failures: Union Carbide returned USD 87,000,000 against label-based USD 5,842,000,000, Echo Global Logistics returned no rows against USD 1,512,298,686, and FutureFuel returned USD 69,306,000 against USD 66,893,000. Preserve and investigate these under full evaluation.

Ran the normal default command for Birner and Solera. Both completed with provenance and matching SQL re-execution. Solera's answer used custom tag `RevenueSoftwareHostedSoftwareDeliveryImplementationAndMaintenance`, filing `0001324245-16-000077`, 10-Q filed 2016-01-29, quarter ending 2015-12-31. An empty-map check still answered a standard Assets question successfully. This seven-question result is a focused integration check; the full 151-question ladder is pending.

Code and both READMEs are saved locally. Recent work remains uncommitted. Next package the independent golden-set generation and run the complete five-rung answer evaluation, including held-out wording.

### Full fixed-reference answer evaluation completed

Added `src/sec_analyst/golden.py`, preserving the notebook's reference-answer rules, source revenue-line selection, sampling and development/held-out question templates with explicit inputs. Added `n_per_cell: 12` to configuration. Added `src/sec_analyst/evaluate_answers.py` to prepare the reference set, map custom income-statement tags and run every question through all five rule levels, followed by alternate wording. Run from the repository root with `python3 -m sec_analyst.evaluate_answers`.

An initial generation on the new prepared files produced fingerprint `0713784cea379601b402812baf745c1790be4d4eaac43136c56bad28171f158f`. Original notebook functions and packaged generation produced exactly equal fingerprint columns on those inputs. Repeating generation matched that saved set. Running the original code on Nathan's original notebook files reproduced `d9687a7d2ce416a9df0a30141527ade4dbb474294eaeb52188eacdddee12a2d4`. Ten sampled NetIncome questions differed, comprising three fiscal and seven quarterly questions. The eligible flow data had the same 51,356 records after sorting but a different order, so the original position-based seeded sample selected different questions. Balance-sheet facts and revenue-selection frames matched including row order.

Saved Nathan's earlier exact 151-question set and manifest under `tests/fixtures/`, where they can be versioned. The normal evaluation now reads this fixed set and verifies its fingerprint. `--rebuild-golden` explicitly generates a replacement from configured files. Documented this decision and its tradeoffs in `docs/decisions/0001-freeze-golden-questions.md`. The notebook's published `0c4d749d61487864…` hash remains an observed difference from Nathan's run.

The fixed-reference run used 735 custom income-statement items, 45 mapped to revenue members, and completed 755 development answer checks. Overall R0–R4 results on newly prepared files were 38.4%, 69.5%, 84.8%, 94.7%, 97.4%. Final development result 147/151, interval 93.4%–99.3%, comprising 147 correct, two wrong numbers and two unanswered. Held-out wording returned 128/151 correct (84.8%), two wrong numbers and 21 unanswered; failure statuses were 19 not understood, two no rows and two answered incorrectly. These final figures and later rule levels match Nathan's original notebook run.

Investigated early-rule differences. Original notebook functions on original files reproduced R0 37.1% and R1 68.2%; all 302 original-versus-packaged early-level answers on those inputs matched. The weak templates can choose different tied facts when prepared-file row order changes. Oncor's same 10-Q contains USD 948 million for one quarter and USD 1,891 million for two quarters at 2016-06-30. R0 picks different durations on the two inputs; R2 requires a single quarter and returns USD 948 million on both. Preserve the given method and report this sensitivity.

Saved the golden-set copy, per-question expected/actual answers and SQL, accuracy ladder, metrics with settings/Python/package versions, and comparison evidence under ignored `data/evaluation/`. The final run spent 0.10s loading/checking the fixed reference, 10.07s on custom mapping including mapper build and line-item setup, 16.33s on development evaluation and 0.25s on held-out evaluation. The `reference_preparation` timing includes loading and checking the fixed set, or generation when explicitly requested. Both existing loader tests passed. Both READMEs and all code are saved locally; recent work remains uncommitted. Next review remaining failures and package the notebook's answer/referral policy before operational deployment. The input-order investigation is evidence for RD1 reproducibility discussion.

### Referral policy reproduced and progress audited

Added `policy.py` and `evaluate_policy.py`, preserving Section 6 signals and the three policy calculations with explicit service/configuration inputs. Added the notebook cost assumptions to YAML. Run from the repository root:

```bash
python3 -m sec_analyst.evaluate_policy
```

The command loads the fingerprint-checked fixed questions, prepares the same custom mapping scope, evaluates both phrasings and writes `policy_answers.csv`, `policy_comparison.csv`, `wrong_verified_answers.csv` and `policy_metrics.json` under ignored `data/evaluation/`. Development: 126 filtered answers, one wrong; held-out: 115 filtered answers, one wrong. Both wrong rows concern FutureFuel. Restatement flags: 12 of 279 answered questions across the two phrasings. Policy costs and break-even match the notebook: EUR 3,500 analyst-only; filtered EUR 2,566 development/EUR 2,821 held-out at observed rates, versus EUR 9,865/EUR 10,107 at the 95% upper error bounds. Break-even is 1.17%, requiring 256 shown answers if zero errors; current samples do not establish it. These are assumptions-based modeled costs, excluding infrastructure.

Checked all 302 signal outputs and all six policy summaries against the original notebook functions: all matched. Both existing loader unit tests passed and `git diff --check` passed. These compatibility checks are distinct from the still-pending automated trap regression suite. No model tuning or original notebook edits. No commit was made.

The no-wrong-verified-answer release criterion currently fails; it is reported as false in metrics, not implemented as CI enforcement yet. The notebook's aggregate checks and non-blocking restatement flag are preserved. ADR 0002 records the limitations; operational approval and C3 sensitivity remain pending. `ask` remains the diagnostic answer command; this step evaluates referral rules and does not yet add a gated HTTP service.

Corrected stale opening status text. The requirements audit in `fin-analyst/docs/progress.md` (or `docs/progress.md` from the repository) estimates RD1 readiness at about 25% and full required project completion at about 20%, with explicit outstanding work. Next: data-trap regression tests and evidence table, Git checkpoint, then POST /ask, container, fresh-copy reproduction, monitoring/load measurements and RD1 reasoning/reflection.

### API and Docker implemented and checked

Added `src/sec_analyst/api.py` (FastAPI/Uvicorn), `Dockerfile`, `.dockerignore`, `compose.yaml`, request/filter tests and `scripts/check_api.py`. Added pinned API/test dependencies. Startup loads the original mapper once; `prepare_custom_map` accepts that existing mapper without changing scoring. Shared database/map access is serialized and SQL cache cleared between requests. The input is a bounded JSON question, not arbitrary caller SQL. Invalid dates return HTTP 422.

The API returns `decision: refer`, `answer: null`, and the original candidate with evidence because the wrong-verified-answer release criterion remains failed. This review-only serving decision is separate from preserving/evaluating the given model. `/health` reports readiness and `/docs` provides an interactive form.

Docker image `fin-analyst:rd1` built successfully for Linux ARM64, using Python 3.14.0 pinned by digest and pinned dependencies. An initial missing setuptools backend was fixed explicitly. Host port 8000 was occupied, so Compose maps localhost:8008 to internal port 8000. Prepared data is mounted read-only, excluded from the image. Six tests pass locally and in the container. Five HTTP response bodies exactly match saved local API results: Birner, custom Solera, known wrong FutureFuel, unsupported wording and invalid date. The container is healthy and left running for Nathan at http://localhost:8008/docs. Stop it from the repo with `docker compose down`.

Image inspected size: 1,203,599,174 bytes (~1.20 GB). Image ID and evidence are recorded in `docs/evidence/api-container-check.md` within the repo. Learning instructions: `docs/api-and-docker.md`; design decision: ADR 0003; initial data-quirk table: `docs/evidence/data-quirks.md`. These are focused checks, not realistic load/p95 or a full served golden-set evaluation. Original notebook unchanged; no Git commit made. Both READMEs and progress audit updated. Approximate readiness is now RD1 50%, whole required project 30%; remaining work includes fresh-clone/full reproduction, further convention tests, monitoring/load, architecture/governance and Nathan's reflection deliverables.
