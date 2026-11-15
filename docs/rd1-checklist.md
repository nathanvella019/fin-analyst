# RD1 remaining checklist

Checked 15 November 2026 against the supplied `ARI3217 Reflective diary.pdf` (Entry 1) and `task-rubric.md`. Deadline: Monday 23 November 2026. This lists RD1 work, not the entire final project. Current readiness estimate of about 65% is rough and is not a predicted mark.

## Already demonstrated

- [x] Packaged given method, configuration and runnable commands; original reference notebook preserved.
- [x] Ten tests pass; initial SQL-trap regression tests exist.
- [x] Headline mapper/answer metrics and mapper build/evaluation times recorded.
- [x] Fresh local clone and clean Linux build reproduce final results; commit `f937aba`, evidence commit `64decc3`.
- [x] Docker service, image size/identity, fixed reference fingerprint and full served/offline comparison recorded.
- [x] Local dashboard measures requests, timing and question length; request metadata persists.
- [x] Sequential timing sweeps and a short 150/hour paced sample recorded, with limitations.
- [x] Additional row-order/sampling quirk investigated; early-rung differences and known FutureFuel failure documented.

## 1. Finish the technical evidence

- [ ] Create a **thin project notebook** that calls package functions rather than containing the implementation. Keep the supplied notebook as the unchanged reference.
- [ ] Finalize the **data-quirk table**: at least three card-listed quirks plus the additional investigated quirk. For each give the card claim, measured count, consequence, and exact test/input check. Link counts to runnable queries or saved evidence and a commit. Existing trap tests count toward this; RD1 does not require finishing the entire final-project C1 suite.
- [ ] Add or verify a **forward-in-time evaluation** following the notebook's rules. The general diary instructions explicitly require evaluating forward in time. The current company-held-out mapper split and alternate wording do not substitute for a temporal test. The earlier notebook quarterly observations are recorded, but their repeatable project evidence still needs checking.
- [ ] Complete the **versioned prediction audit**: current persistent metadata has version/status/timing/length, but omits the proposed value and filing source. Add an auditable prediction record, distinguish review candidate from released answer, and identify the tested commit/image. Do not claim the 0.1.0 package string alone uniquely identifies every working-tree revision.
- [ ] Finalize and justify the **realistic workload** and p95 evidence. Ten paced observations make p95 equal the maximum; strengthen the sample or explain that limitation honestly. Distinguish 150/hour serving traffic from 150/week in the economic assumptions.
- [ ] Capture **one readable dashboard panel** showing the measured run. Preserve a screenshot for the written entry/slides; ensure its version/session and counts can be explained.
- [ ] Assemble **one service-results table**: headline accuracy, mapper build time (given model fitting), fresh-copy result, image size, client p95/workload, tested commit/image and limitations. Select consistent evidence versions and preserve R0/R1 differences rather than blending runs.

## 2. Explain the architecture and choice

- [ ] Draw the **four EA layers**: business, data, application and technology. Locate the Python package, API, container, DuckDB/Parquet, dashboard and the person acting on the result.
- [ ] Name the task's actual **capability patterns**: batch data preparation plus online question answering with human review; verify wording against the task card/session material.
- [ ] Compare against **one alternative**, such as automatic answers versus human-reviewed answers, in a side-by-side table covering all four required points: latency budget, running cost per day, decision owner and failure handling.
- [ ] Calculate/estimate **daily running cost**, stating assumptions and what is included. Existing weekly wrong-answer/referral costs are not measured infrastructure running cost. Do not invent a measured hosting cost for the local Mac.
- [ ] State the **chosen pattern, reasons and switch condition**: which measured threshold or new evidence would make the alternative preferable?

## 3. Complete the EU AI Act reasoning

- [ ] Consult current authoritative legal sources for the intended use.
- [ ] Identify the risk tier, supporting article/annex, provider and deployer.
- [ ] Explain how the classification could change with deployment use, including any use involving natural-person creditworthiness. Do not assume all financial software has the same tier.
- [ ] Produce the required concise classification line with a citation. No legal classification has been completed yet.

## 4. Write Nathan's reflection

- [ ] Gather Nathan's own views and address **at least three supplied reflection prompts**; write about decisions and learning rather than narrating code.
- [ ] Explain something that broke/surprised him, the consequence if missed, and what he learned. Available evidence includes tied-row selection, missing setuptools in Linux, and a wrong FutureFuel answer passing checks.
- [ ] Explain what a healthy dashboard cannot reveal about financial correctness.
- [ ] State what evidence would change his mind and what he would do next.
- [ ] Disclose AI assistance for code/language and keep the reasoning genuinely Nathan's.

## 5. Produce and submit the three parts

- [ ] Written entry: **400–600 words**, excluding tables, figures, code and references; export PDF.
- [ ] Include the required evidence: quirk table, service table + dashboard panel, four-layer diagram, two-pattern comparison table and classification line.
- [ ] Slides: **5–8 content slides**, with optional title/reference slides; export PDF. Present the same investigation, not new unsupported results.
- [ ] Video: **at most five minutes**, Nathan's own voice; present slides and showcase the service. Appearing on camera is optional.
- [ ] Check every number and version across text, slides and video against the same evidence; clearly identify known failures and sample limits.
- [ ] Save final code/docs/evidence checkpoints and check the VLE's upload/link instructions. The local rubric heading says ARI3218 while the brief says ARI3217; confirm the applicable marking guidance.
- [ ] Submit written PDF, slides PDF and video file/link by **23 November 2026**.

## Keep scope under control

RD1 does not require completing all C1–C5/E1–E4/S1, implementing the LLM, building the RDF graph, finishing knowledge-base ablations or completing Entry 2's MLflow/public-repository work. A full raw-data contract and full C1 independent convention suite remain final-project work; only extend them now where needed to support the RD1 checks. An honest review-only service can support RD1: disclose the known wrong verified answer rather than claiming operational release.

Recommended order: close technical evidence -> architecture/comparison -> legal reasoning -> Nathan's reflection -> PDFs/video -> consistency/submission checks.
