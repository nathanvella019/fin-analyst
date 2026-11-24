# RD2 Task 4 — Registered mapper and rollback

The local MLflow registry holds two usable versions of `sec-standard-tag-mapper`. Each one contains the fitted vocabulary, tag index and prediction code. Loading a version takes three input columns (custom tag, statement label and statement type) and returns five ranked tags. It can score new rows without opening DuckDB or fitting the mapper again.

| Build | Eligible filings used | First suggestion correct | Correct in first five | MLflow run |
|---|---:|---:|---:|---|
| Through 29 February, version 1 | 3,258 | 95/345 (27.54%) | 191/345 (55.36%) | `7544afb5e79542c0907469a0bfda8024` |
| Through 31 March, version 2 | 6,022 | 115/345 (33.33%) | 201/345 (58.26%) | `433508d40ff64b7a9beff45d995f7f96` |
| March rebuilt in a fresh process | 6,022 | 115/345 (33.33%) | 201/345 (58.26%) | `9e9bc1fbf997480ba1be2e4189404a4b` |

The cutoffs use the date a report was filed. Both builds excluded the same 486 test companies. For February we also restricted the quarterly taxonomy dictionary to tag/version pairs seen in eligible filings by 29 February. For March we used the original Q1 input preparation. Its training-input fingerprint and ordered predictions matched the earlier Q1 reference. All three builds used the same 345 later cases. The expected tags are inferred from subsequent filings, so the scores describe this particular benchmark.

**Rollback evidence.** We loaded each saved model in a separate demonstration process and checked all five ranks for every case against its training record. We then requested the model by its alias, `models:/sec-standard-tag-mapper@champion`, at each step.

| Action | Alias resolved to | Check |
|---|---|---|
| Select March | Version 2 | All 345 ordered lists matched March |
| Roll back to February | Version 1 | All 345 ordered lists matched February |
| Restore March | Version 2 | All 345 ordered lists matched March |

Repeating the drill reused the same versions. A further load from an empty working directory used the prediction code bundled with the saved champion. The API continues its existing review workflow. This exercise changed the local registry only.

**Trace.** Training commit `32d16c6`. Repeat-drill version handling `12a5f5f`. The local full CI check on the training commit passed, MLflow gate run `fffd9ff6ce09428db54ea0aea7b5fc5d`. The registry and fitted artifacts live under ignored `data/rd2-tracking/` in the Task 4 worktree. The committed JSON has the run IDs, exact metrics, fingerprints and alias history. [Registry results](registry-results.json) · [Decision](../../decisions/0014-local-mapper-champion.md)

## Reproduce locally

From the project root, use the RD2 project environment with the four prepared quarters. Each fit command starts a separate Python process and prints a new run ID.

```bash
python -m sec_analyst.rd2_registry fit february
python -m sec_analyst.rd2_registry fit march
python -m sec_analyst.rd2_registry fit march --repeat
```

On a fresh registry, pass those three IDs to the following command in build order. On Nathan's existing registry, the command below repeats the drill with the saved runs. It finishes with March as champion.

```bash
python -m sec_analyst.rd2_registry demo 7544afb5e79542c0907469a0bfda8024 433508d40ff64b7a9beff45d995f7f96 9e9bc1fbf997480ba1be2e4189404a4b
```
