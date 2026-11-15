# Reproducing from a fresh local clone

Run from `fin-analyst`, with Docker Desktop running and the host `.venv` active:

```bash
python3 scripts/reproduce.py --raw-dir "../archive (1)"
```

This is a substantial check: it builds an image without reusing build steps, installs pinned dependencies, converts all four raw quarters into a separate empty output folder, runs the tests and reproduces mapper, answer and referral evaluations. It can take several minutes and needs network access during image/dependency installation. Runtime containers have networking disabled and read the provided raw files read-only.

The script clones **HEAD**, the saved commit, rather than copying uncommitted changes. Commit intended source changes first. It records that commit, SHA-256 fingerprints and sizes of the four raw JSON files, the resulting image identity, stage exit codes and timings. It does not regenerate the fixed reference questions: those are deliberately versioned to prevent sampling changes from changing the benchmark (ADR 0001).

The clone, generated files, logs and manifest are under ignored `data/reproduction/<commit>-<unique-folder>/`. The main project's prepared data and running Compose service are not replaced. Input path changes live in a separate mounted configuration file; the cloned source/configuration stays unchanged. Linux paths replace the Mac-specific raw-data path. This is a fresh local clone/environment reproduction using existing raw inputs, not a demonstration of public remote-clone or Kaggle download access.

The script asserts exact baseline dataset counts, 147/151 final development answers, 128/151 alternate phrasings and the fixed golden fingerprint. Mapper results and all rung results are recorded in logs for comparison; differences must be examined, not hidden. Early-rung row-order sensitivity remains documented. The final answer gate is still blocked by the known wrong verified candidate even when baseline reproduction succeeds.

Each run retains its files and a tagged image. They consume disk space. Do not delete the original raw data or main project outputs when cleaning reproduction artifacts later. Evidence intended for submission is summarized separately under `docs/evidence/`, tied to the tested commit and image.
