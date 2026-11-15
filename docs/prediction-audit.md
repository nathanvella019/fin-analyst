# Prediction audit: how to trace an answer

Implemented in revision `7552b91` without changing the model. Each `POST /ask` receives a UUID in its `X-Request-ID` response header. Match that ID with a line in Docker's `/app/data/logs/requests.jsonl`.

The saved line records the proposed value, filing provenance, generated SQL, screening flags and actual decision/released answer. For industry aggregates there is no single filing; the generated query describes the selected sources. Every result remains a candidate, `decision` is refer and `released_answer` is null in this deployment. Unsupported questions also have an audit event; they have no proposed number. Invalid inputs and server errors have HTTP outcome/timing records.

Identity contains package version, supplied code revision, source fingerprint, configuration fingerprint and golden-set fingerprint. The evidence report maps that identity to the image ID. The source fingerprint is checked against the host's package files. The code revision is a build annotation; it must be supplied correctly, and an unknown value must not be presented as a clean commit.

The audit intentionally omits raw question text. Unlike the earlier request-metadata format, the new format includes public SEC-derived financial values, filing IDs and generated SQL. Do not claim it contains no financial values. Do not interpret a log line as permission to release a number or as a correctness label. Failed writes are counted and reported; verified zero write failures and request-ID reconciliation are part of the RD1 experiment evidence.

The named `request_logs` volume survives ordinary shutdown. It currently has no automatic rotation. The directory can contain old-format records from earlier sessions; use session/revision/request ID to select the intended experiment. Do not pool unrelated sessions or silently discard known mistakes.
