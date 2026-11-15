# Understanding the RD1 technical evidence

## Thin notebook

`notebooks/analyst_client.ipynb` imports the package. The package is the single implementation of the given model; the notebook is a way to run and inspect it. Four code cells load configuration, inspect concepts, run accounting identities and ask Birner's revenue question. Repeat their execution with `python3 scripts/verify_notebook.py` from the repo root. They have been executed sequentially in project Python. No original notebook code was edited.

## Data checks

`python3 -m sec_analyst.data_checks` reruns SQL on the actual prepared tables. Synthetic regression tests do something different: they construct tiny deliberately misleading rows and verify that removing a filter admits the wrong context. Counts show the problem exists; tests protect the rule we use to handle it. These checks do not claim that every filing is correct.

- `qtrs`: distinguish one quarter from six months or a year.
- `coreg`: distinguish the main reporting company from a co-registrant.
- `uom`: keep compatible currency units.
- Filing/period selection: avoid replacing original-period figures with later comparative figures.
- `fy`: use the company's fiscal-year label rather than assuming December year ends.

See `docs/evidence/data-quirks.md` for counts, exact test names and consequences.

## Looking forward in time

`python3 -m sec_analyst.evaluate_temporal` first repeats the notebook's quarterly diagnostic: freeze the reference index at Q1, then test tags first seen in later quarters. Refreshing the index gives a comparison. Companies used for testing stay out of the honest index; a deliberately leaky index shows the danger of including them.

The notebook still fits the word vocabulary from the full year. We disclose that and run a separate sensitivity check with the same algorithm restricted to line items and taxonomy metadata available by the cutoff. Silver reference labels are inferred retrospectively. This is a historical quarterly evaluation with stated limits, not a real prospectively frozen 2016 deployment. The stricter input check is not a replacement champion model.

## Audit records

Each POST /ask has a UUID returned in `X-Request-ID`. The persisted JSONL record links that request to the proposed value, source filing or generated aggregate query, screening flags and actual review decision. A proposed value is not a released answer: `released_answer` stays null in review-only mode.

Identity includes package version, supplied build revision, Python-source fingerprint, configuration fingerprint and fixed golden fingerprint. The report maps these to Docker image identity. Logs do not retain raw question text; they now do retain public financial candidate values and generated SQL. Earlier metadata-only logs used a smaller format. Normal shutdown keeps the named volume; no automatic log rotation exists yet.

To build with a known revision, first commit intended implementation changes, then set its revision in the build command (for example `FIN_ANALYST_REVISION=7552b91 docker compose up --build -d --wait`). Do not label a dirty source build with a clean revision. The source fingerprint provides an additional content check.

## Measurements

The final RD1 run uses a declared busy-period scenario: six analysts each sending one question per minute, for 60 requests at 360/hour over nearly ten minutes. This is a design assumption, not observed user traffic. It strengthens the earlier ten-request 150/hour smoke test. We keep the two rates and results separate. Scheduled arrivals, full response timing, HTTP errors and client scheduling delay are recorded. P95 on 60 requests is the fourth-largest observation using the nearest-rank rule; sampling uncertainty remains.

The rolling dashboard describes its own request window. The client experiment records a specific workload and includes the HTTP round trip. Therefore their p95 values need not be identical. Neither is a financial-accuracy measure.

No architecture choice, legal classification or personal reflection is supplied by these technical checks. Those remain Nathan's next RD1 tasks, using this evidence.

Application handling time is sampled before appending its audit line. Client round-trip timing includes that append and response delivery. This is another reason dashboard and client p95 can differ.
