# RD1 remaining checklist

## Six-task review · 19 November 2026

Deadline: Monday 23 November 2026. The six investigations have evidence. Nathan’s review of the reflection, the final written PDF, slides and video are still pending.

| Task | What was checked |
| --- | --- |
| 1. Given model | The notebook and package use the same two TF-IDF signals and statement filter. The training command is `python3 -m sec_analyst.evaluate_mapper` from the repo root after data preparation. It reads YAML, fits the mapper in memory and scores it. The saved clean-run log gives 6.32 seconds to fit and 1.18 seconds to score. The thin client calls package functions. All ten local unit tests passed again on 19 November. |
| 2. Data traps | All seven groups of saved SQL results matched a fresh read of the configured Parquet files. Page 2 covers three numbered card items: units (3), fiscal years (4) and duplicates (5). Two examples illustrate item 5. The extra finding concerns row order. The SQL tests check that removing a context filter admits a wrong figure. |
| 3. Reproduction and container | The saved clean-build manifest passed for `7552b91`. The serving image is 1.20 GB. Training, offline answering and the API share line-label preparation and mapper code. The held-out evaluation deliberately restricts the search index, while the API builds the full index at startup. All 302 served and offline outcomes matched. The final score reproduced. Earlier query ties and differences from the notebook’s printed summary remain documented. |
| 4. Monitoring | The API records proposed answers and model identity. Metrics include requests, elapsed time and question length. Recounting the saved request files gave 362 distinct IDs. Recalculating p95 for the 60 warm busy-period requests gave 181.4 ms. The earlier Docker run supplies the deployment evidence. |
| 5. Architecture and decision | ADR 0008 shows the four layers. It compares analyst review and automatic release by response time, estimated daily cost, decision owner and failure handling. Human review time and shared IT costs are unmeasured. |
| 6. Classification | ADR 0009 and page 4 give the working tier for a company lookup, the legal basis and both prospective roles. The assessment depends on who supplies the service and what the user does with it. |

## Earlier checkpoints

- [x] Packaged given method, configuration and runnable commands; original reference notebook preserved.
- [x] Ten tests pass; initial SQL-trap regression tests exist.
- [x] Headline mapper/answer metrics and mapper build/evaluation times recorded.
- [x] Fresh local clone and clean Linux build reproduce final results; commit `f937aba`, evidence commit `64decc3`.
- [x] Docker service, image size/identity, fixed reference fingerprint and full served/offline comparison recorded.
- [x] Local dashboard measures requests, timing and question length; request metadata persists.
- [x] Sequential timing sweeps and a short 150/hour paced sample recorded, with limitations.
- [x] Additional row-order/sampling quirk investigated; early-rung differences and known FutureFuel failure documented.

## 1. Technical evidence completed — 15 November 2026

- [x] Create a **thin project notebook** that calls package functions rather than containing the implementation. Keep the supplied notebook as the unchanged reference.
- [x] Finalize the **data-quirk table**: at least three card-listed quirks plus the additional investigated quirk. For each give the card claim, measured count, consequence, and exact test/input check. Link counts to runnable queries or saved evidence and a commit. Existing trap tests count toward this; RD1 does not require finishing the entire final-project C1 suite.
- [x] Add or verify a **forward-in-time evaluation** following the notebook's rules. The general diary instructions explicitly require evaluating forward in time. The current company-held-out mapper split and alternate wording do not substitute for a temporal test. The earlier notebook quarterly observations are recorded, but their repeatable project evidence still needs checking.
- [x] Complete the **versioned prediction audit**: current persistent metadata has version/status/timing/length, but omits the proposed value and filing source. Add an auditable prediction record, distinguish review candidate from released answer, and identify the tested commit/image. Do not claim the 0.1.0 package string alone uniquely identifies every working-tree revision.
- [x] Finalize and justify the **realistic workload** and p95 evidence. Ten paced observations make p95 equal the maximum; strengthen the sample or explain that limitation honestly. Distinguish 150/hour serving traffic from 150/week in the economic assumptions.
- [x] Capture **one readable dashboard panel** showing the measured run. Preserve a screenshot for the written entry/slides; ensure its version/session and counts can be explained.
- [x] Assemble **one service-results table**: headline accuracy, mapper build time (given model fitting), fresh-copy result, image size, client p95/workload, tested commit/image and limitations. Select consistent evidence versions and preserve R0/R1 differences rather than blending runs.

Completed evidence: [final service table/dashboard](evidence/rd1-service-results.md), [data quirks](evidence/data-quirks.md), [forward-time checks](evidence/forward-time.md), [audit](prediction-audit.md), [thin client](../notebooks/analyst_client.ipynb). Tested implementation `7552b91`; ten tests pass; final fresh clone passes declared final-baseline assertions. Original notebook prose/fingerprint discrepancies and early-rung ordering remain explicitly documented. This completes the RD1 technical-evidence scope, not the entire final project or automatic financial release.

## 2. Explain the architecture and choice

- [x] Draw the **four EA layers**: business, data, application and technology. Locate the Python package, API, container, DuckDB/Parquet, dashboard and the person acting on the result.
- [x] Name the task's actual **capability patterns**: batch data preparation plus online question answering with human review; verify wording against the task card/session material.
- [x] Compare against **one alternative**, such as automatic answers versus human-reviewed answers, in a side-by-side table covering all four required points: latency budget, running cost per day, decision owner and failure handling.
- [x] Calculate/estimate **daily running cost**, stating assumptions and what is included. Existing weekly wrong-answer/referral costs are not measured infrastructure running cost. Do not invent a measured hosting cost for the local Mac.
- [x] State the **chosen pattern, reasons and switch condition**: which measured threshold or new evidence would make the alternative preferable?

Draft assessment/diagram: [ADR 0008](decisions/0008-architecture-and-review.md). Nathan still needs to review the reasoning. Daily workflow costs are assumption-based; shared IT costs remain explicitly unmeasured.

## 3. Complete the EU AI Act reasoning

- [x] Consult current authoritative legal sources for the intended use.
- [x] Identify the risk tier, supporting article/annex, provider and deployer.
- [x] Explain how the classification could change with deployment use, including any use involving natural-person creditworthiness. Do not assume all financial software has the same tier.
- [x] Produce the required concise classification line with a citation. A working classification with scope/definition qualifications is now documented.

Working assessment and official citations: [ADR 0009](decisions/0009-ai-act-classification.md). Nathan should review the reasoning; this is not a regulator determination or full compliance audit.

## 4. Write Nathan's reflection

- [ ] Gather Nathan's own views and address **at least three supplied reflection prompts**; write about decisions and learning rather than narrating code.
- [ ] Explain something that broke/surprised him, the consequence if missed, and what he learned. Available evidence includes tied-row selection, missing setuptools in Linux, and a wrong FutureFuel answer passing checks.
- [ ] Explain what a healthy dashboard cannot reveal about financial correctness.
- [ ] State what evidence would change his mind and what he would do next.
- [ ] Disclose AI assistance for code/language and keep the reasoning genuinely Nathan's.

An initial 400–600-word first-person draft is now filled in at [written-entry-draft.md](rd1/written-entry-draft.md), at Nathan's request. It is explicitly provisional: the personal-review checkboxes stay open until he reviews it. His tasks are pinned in [PENDING_FOR_NATHAN.txt](../PENDING_FOR_NATHAN.txt).

## 5. Produce and submit the three parts

- [ ] Written entry: **400–600 words**, excluding tables, figures, code and references; export PDF.
- [x] Included in the [written preview](../output/pdf/RD1-written-entry-preview.pdf): quirk table, service table + dashboard panel, four-layer diagram, two-pattern comparison table and classification line.
- [ ] Slides: **5–8 content slides**, with optional title/reference slides; export PDF. Present the same investigation, not new unsupported results.
- [ ] Video: **at most five minutes**, Nathan's own voice; present slides and showcase the service. Appearing on camera is optional.
- [ ] Check every number and version across text, slides and video against the same evidence; clearly identify known failures and sample limits.
- [ ] Save final code/docs/evidence checkpoints and check the VLE's upload/link instructions. The local rubric heading says ARI3218 while the brief says ARI3217; confirm the applicable marking guidance.
- [ ] Submit written PDF, slides PDF and video file/link by **23 November 2026**.

## Keep scope under control

RD1 does not require completing all C1–C5/E1–E4/S1, implementing the LLM, building the RDF graph, finishing knowledge-base ablations or completing Entry 2's MLflow/public-repository work. A full raw-data contract and full C1 independent convention suite remain final-project work; only extend them now where needed to support the RD1 checks. An honest review-only service can support RD1: disclose the known wrong verified answer rather than claiming operational release.

Recommended order: close technical evidence -> architecture/comparison -> legal reasoning -> Nathan's reflection -> PDFs/video -> consistency/submission checks.
