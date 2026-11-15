# ADR 0006: Reproduce a saved commit in an isolated Linux environment

Date: 15 November 2026. Status: workflow accepted; outcome recorded in reproduction evidence.

## Decision

Use `scripts/reproduce.py` to clone the current saved commit locally, check out its full hash, build with `docker build --no-cache`, and prepare/evaluate in separate empty directories. Mount only the selected raw JSON source directory read-only. Attach a separate configuration file that changes deployment paths only. Record raw file names, sizes and SHA-256 fingerprints, image ID/size/architecture, command stage timings and exit codes.

The script retains the cloned source unchanged. Containers run with runtime networking disabled, so a passing conversion cannot depend on a hidden Kaggle download. Dependency installation during build still requires registry/package-index access. Docker may already possess the digest-pinned base image; `--no-cache` forces the Dockerfile steps to execute again but does not establish a new machine or a newly downloaded base.

Keep the earlier fixed golden fixture from Git, validating its fingerprint. Do not regenerate or change the benchmark during reproduction. Exact requirements for this four-quarter baseline: 27,677 filings, 7,229 companies, 10,890,076 facts, development 147/151 and alternate wording 128/151. Mapper and full ladder results are logged and compared manually; early R0/R1 ordering sensitivity must remain visible rather than being hidden by a blanket claim of identical outputs.

## Scope and trade-offs

This proves fresh local clone/clean environment reproduction with the existing source data, if the recorded stages pass. It does not prove a remote repository is accessible, that fresh Kaggle credentials work, or that a different architecture yields bitwise-identical artifacts. Full data contracts and independent financial-convention tests remain required. Raw fingerprints are evidence of these inputs, not proof that the dataset is correct.

Outputs, raw hashes and logs are retained under ignored `data/reproduction/`; a concise result report is versioned under `docs/evidence/`. The workflow leaves the main data and running Compose container untouched. Keeping clones/images consumes disk; cleanup is a separate deliberate step after retaining needed evidence.
