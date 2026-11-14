# Freeze the notebook reference questions

Status is accepted for the current baseline.

The original notebook and the packaged generator produce identical questions on the same prepared files. However, the newly prepared files generate fingerprint `0713784cea379601b402812baf745c1790be4d4eaac43136c56bad28171f158f`, while Nathan's earlier notebook files generate `d9687a7d2ce416a9df0a30141527ade4dbb474294eaeb52188eacdddee12a2d4`.

The eligible flow dataset contains the same 51,356 rows after sorting, with a different row order before sampling. The notebook's seeded pandas sampling selects positions within that order. Three fiscal and seven quarterly NetIncome questions change. Balance-sheet facts and the revenue-selection rows match in order as well as content.

Save Nathan's earlier 151-question reference set under `tests/fixtures/golden_questions.parquet`, with its fingerprint and generation settings in `golden_manifest.json`. The evaluation command reads that fixed set by default and checks its fingerprint. The `--rebuild-golden` option explicitly generates a replacement from the configured files.

This keeps the source model, filtering rules, sampling rule and seed intact while allowing repeated evaluation on the same questions. The saved set and manifest belong in version control. Evaluation results remain under the ignored `data/evaluation/` folder. Rebuilding the set creates a new benchmark version and requires documenting its fingerprint and comparing results.

The notebook's published fingerprint `0c4d749d61487864…` still differs from Nathan's observed notebook run. This decision preserves Nathan's observed baseline and records that outstanding difference.

Further checks also found that the weak R0 and R1 queries can select different tied rows on the two prepared folders. The original functions on the original files reproduce Nathan's observed 37.1% and 68.2%. All 302 early-level original-versus-packaged answer comparisons match on those inputs. With the fixed questions and new files, the scores are 38.4% and 69.5%. R2 through R4 remain 84.8%, 94.7% and 97.4%.

For Oncor revenue ending 30 June 2016, the same filing contains USD 948 million for one quarter and USD 1,891 million for two quarters. R0's ordering permits either duration. R2 requires one quarter and selects USD 948 million on both inputs. Preserve the given templates and record this input-order sensitivity in baseline evidence.
