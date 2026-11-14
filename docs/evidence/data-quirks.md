# Data checks and their consequences

The real-data observations below are Nathan's recorded notebook outputs. The new regression tests deliberately use tiny synthetic data so the cause of each failure is easy to see; they do not remeasure the full dataset counts.

| Quirk | Recorded observation | Consequence | Current protection |
| --- | --- | --- | --- |
| Reporting duration | 11,365 10-Qs have two net-income durations at the same date | Six-month figures can answer a three-month question incorrectly | Synthetic test proves removing `qtrs = 1` admits an incorrect figure |
| Different reporting entities | 20.4% of Assets facts belong to a co-registrant | A subsidiary figure can be confused with the main company | Synthetic test proves removing `coreg IS NULL` admits a subsidiary value |
| Currency | Annual Revenues sums: all units 75.0 trillion vs USD-only 8.5 trillion | Yen, dollars etc. cannot simply be added | Synthetic test proves removing `uom = 'USD'` admits a JPY value |
| Original reporting context | Apple repeats 2015-09-30 assets with a later changed value | A later comparative figure can replace the original figure | Test proves removing `n.ddate = s.period` admits a later comparative; annual fixture excludes a 10-K/A |
| Fiscal year | 467 of 6,382 10-Ks have fiscal year differing from period-end calendar year | Calendar-year filtering misses the intended annual report | Fixture checks March 2016 year-end labelled fiscal 2015; R3 finds it while R2 misses it |
| Additional investigated quirk: row order | Ten sampled NetIncome questions changed when eligible row order changed; sorted records were identical | A fixed random seed alone does not fix the benchmark; weak tied SQL selection can also change | Fingerprinted fixed question fixture; ADR 0001 and comparison evidence |

Still needed for full C1/C2: independent convention tests, broader mutation coverage, explicit parent/subsidiary industry-sum policy, raw-input schema/range contract, and refreshed full-data evidence tied to a commit. The full source models and conventions remain unchanged.
