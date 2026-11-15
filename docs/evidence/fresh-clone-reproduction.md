# Fresh-clone reproduction — 15 November 2026

Tested commit: `f937aba62a03862ea9e0bb90ff67f776e8093f68` (`f937aba`). Result: **passed the declared final-baseline assertions**, with documented early-rule differences.

## Isolation and inputs

Cloned the saved local Git repository into a new folder and checked out the exact commit. Built the Dockerfile with `--no-cache`, reinstalling all pinned dependencies in Linux ARM64. Existing digest-pinned base layers could be reused. Mounted four raw JSON files read-only, fingerprinted them, and generated all prepared files/caches into an initially empty separate folder. Runtime containers had networking disabled. Deployment paths changed through a separate mounted YAML; source code/model settings did not change. The main Compose service and prepared data were not replaced.

Image ID: `sha256:e29ce6a19cec3b5d520d80e0bd7a533d9d01ea1d59442ac9a83e7d979d3260cd`. Inspected size: 1,203,796,572 bytes. One-off containers used two CPU quota and a 3 GB memory limit. This is a fresh local clone and clean environment with existing raw data, not proof of remote repository/Kaggle download access or another hardware architecture.

## Results

| Check | Reproduced result |
| --- | --- |
| Unit tests | 10 passed |
| Filings / companies / numeric facts | 27,677 / 7,229 / 10,890,076 |
| Company-held-out mapper | 486 of 972 companies; 702 test tags |
| Mapper index | 270,660 tag/label pairs; 6,067 candidate tags |
| Baseline mapper top-1 / top-5 | 32.5% / 60.5% |
| Mapper top-5 interval | 56.8%–64.2% |
| R2 / R3 / R4 accuracy | 84.8% / 94.7% / 97.4% |
| Final development accuracy | 147/151, interval 93.4%–99.3% |
| Alternate wording accuracy | 128/151 (84.8%) |
| Custom IS items / revenue mappings | 735 / 45 |
| Referral policies | All six summaries match the main project exactly |
| Release criterion | Still fails: two wrong-verified rows, the same FutureFuel fact under two phrasings |

The fixed golden fingerprint is `d9687a7d2ce416a9df0a30141527ade4dbb474294eaeb52188eacdddee12a2d4`. All candidate values/statuses/correctness match at R2–R4 (453 comparisons) and on all 151 alternate phrasings.

## Differences and acceptance limits

Fresh R0 accuracy is 39.1% versus 38.4% in the main prepared files; seven returned values and five correctness flags differ. R1 remains 69.5% overall, but eleven values and ten correctness flags differ, cancelling in the aggregate score. No statuses changed. This is consistent with the previously investigated early-query row-order/tied-selection sensitivity (ADR 0001); unchanged aggregate accuracy alone does not prove per-question reproduction. R2–R4 values match exactly. The given templates/model are preserved and this limitation remains visible. No blanket claim of identical five-rung outputs is made.

## Timings

These are stage wall times on this Mac, not API latencies or pure training times.

| Stage | Seconds |
| --- | ---: |
| clone | 0.07 |
| checkout | 0.01 |
| build | 110.59 |
| prepare | 53.81 |
| tests | 2.13 |
| mapper | 14.83 |
| answers | 16.77 |
| policy | 13.53 |
| assertions | 0.42 |

Mapper internal build time was 4.30s and scoring 1.25s. Timings vary with environment and cache state; score reproduction is the acceptance criterion, not equal runtime. Raw SHA-256 hashes/sizes, full tested commit, image and stage outcomes are versioned in [reproduction-manifest.json](reproduction-manifest.json).

Full logs and independent prepared/evaluation artifacts remain under ignored `data/reproduction/f937aba-086oonfv/`. Repeat with `python3 scripts/reproduce.py --raw-dir "../archive (1)"` from the repository root. New runs use their current saved HEAD and create a new folder/image. Keep raw-data contract work and independent convention tests on the remaining-task list; this run does not complete C1/C2 or authorize automatic answer release.
