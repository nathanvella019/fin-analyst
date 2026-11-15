# ADR 0007: Complete RD1 technical evidence without replacing the model

Date: 15 November 2026. Status: accepted for the RD1 investigation.

## Decisions

- Add `notebooks/analyst_client.ipynb`, which calls package functions. Keep the supplied reference notebook unchanged. Verify its four code cells sequentially in the project Python environment; do not claim a browser/kernel test from that execution alone.
- Remeasure listed data quirks with runnable SQL in `sec_analyst.data_checks`. Keep initial regression tests that deliberately demonstrate the effect of missing filters. Keep the separately investigated order/sampling quirk and its known limits.
- Preserve Section 7's temporal mapper diagnostic exactly in intent: held-out companies never enter its honest index, with frozen-Q1/refreshed index comparisons and the deliberately leaky comparison. Explicitly disclose the full-year vocabulary fit used by that notebook diagnostic.
- Add a separate same-algorithm input sensitivity check with vocabulary, line items and taxonomy metadata restricted to the available quarter. No learner or score rule changes. Evaluate future-quarter custom tags with retrospective silver references. This is a historical forward-quarter evaluation, not a claim of a fully prospective benchmark; silver-label selection and concept choices remain retrospective.
- Extend audit records to proposed value, filing provenance, generated SQL (needed for aggregates), screening flags, released answer, request UUID and model identity. Keep raw question text out of the audit. Financial candidate values are public SEC-derived results; previous statements that no financial values are logged apply to the earlier request-metadata format only.
- Include exact revision supplied at build, source-code SHA-256, configuration SHA-256 and golden fingerprint alongside package version. Link image identity externally to the tested revision in the report; an image cannot contain its own content hash. Unknown revision is labelled unknown, not inferred to be clean.
- Strengthen measurements with a planned ten-minute busy-desk scenario: six analysts each sending one question per minute, 60 scheduled requests at 360/hour. This is a declared design scenario, not observed organizational traffic. Include all six question families and record dispatch delay. Earlier 150/hour ten-request sample remains separate. Follow with the full fixed-set served checks against the identified image.

## Acceptance and limits

Verify exact data measurements, source-notebook temporal scores and unchanged baseline answering. Unit tests check the new audit identifiers/provenance. Store individual timing rows, source/image identity, summary table, screenshot and observed log reconciliation. Compare all experiment request IDs against persisted audit records. P95 from 60 requests still has sampling uncertainty and does not certify sustained production capacity. A healthy dashboard does not prove financial accuracy. Review-only serving remains mandatory for this demonstration due to the known wrong verified baseline answer.

RD1 technical evidence can be complete while final-project C1/C2 raw contracts, full convention suite and CI/registry/graph/LLM tasks remain outstanding. Reflection, architecture and legal reasoning are separate RD1 deliverables.
