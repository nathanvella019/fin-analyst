# 0011 — How we will compare the random and forward mapper splits

Nathan approved decisions 1–9 on 23 November 2026. The complete plan is ready for review before implementation.

| Decision | What we agreed and why |
|---|---|
| 1. Test the tag mapper | Score how often the expected standard tag appears among the first five suggestions. The existing 151 questions separately test whether the full service returns the correct financial answer. |
| 2. Set the time boundary | For the forward run, build the vocabulary and search index with filings available through 31 March 2016. Test examples first seen from 1 April through 31 December. Use filing availability to determine what the mapper could know. RD1 already examined these quarters, which we will disclose. |
| 3. Split by company | Reuse the notebook’s seeded selection of whole test companies. Keep their examples out of the search index in both runs so repeated wording from the same company cannot supply the match. |
| 4. Compare on common examples | Report the full-year random-company score and the forward score. Also score the full-year mapper on the exact later examples used for the forward run. That comparison holds the test questions fixed while changing the learning window. RD1 had 702 full-year test cases, including 345 later cases (190, 85 and 70 in Q2–Q4). These are RD1 reference counts, pending verification when freezing RD2. |
| 5. Exclude test companies during vocabulary fitting | Both runs learn word patterns from eligible training companies only. The mapper reads the held-out label when asked to predict. This is stricter than RD1 and can change the score even with the same matching code. |
| 6. Use later filings to infer scoring labels | Later re-tagging may identify the expected standard tag. Use that inferred answer only to score a prediction. These “silver labels” can be wrong, and the scores describe the cases for which this evidence exists. |
| 7. Save the holdout and its fingerprint | Save each test company's ID, custom tag, line label, statement type, first-seen quarter and expected standard tag. Write the rows in a fixed order. Record the holdout start date and SHA-256 in configuration so later scoring runs can identify the exact saved file. |
| 8. Stop on a fingerprint mismatch | Verify the file before scoring. If it changes, stop and report the mismatch. For an intentional correction, keep the original, save a new version and document why. |
| 9. Track each fitted mapper separately | Use one local MLflow run per fit. Log the Git commit, learning window, company split, training-input and test-set fingerprints, number correct and number tested. The full-year run records both its full test score and its score on the shared later cases. The Q1 run records its score on those same later cases. |

## Implementation plan awaiting approval

1. Recreate the seeded company split, verify the case counts, and freeze the later test cases before fitting either mapper.
2. Set up local MLflow tracking and verify the holdout fingerprint before scoring.
3. Fit the supplied mapper twice using the approved company and date restrictions. Record both runs and their scores.
4. Produce a comparison table with the dates, counts, top-five accuracy and MLflow run IDs. Verify that the shared-case scores use the same holdout fingerprint and that an altered copy is rejected.

[RD1 quarterly evidence](../evidence/forward-time.md) · [Earlier decision on the 151 questions](0001-freeze-golden-questions.md)
