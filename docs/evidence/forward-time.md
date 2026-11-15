# Forward-quarter mapper evidence — 15 November 2026

Tested revision `7552b91`. Repeat: `python3 -m sec_analyst.evaluate_temporal`. Exact results: [rd1-temporal_mapper.csv](rd1-temporal_mapper.csv); setup/identity: [rd1-temporal_metrics.json](rd1-temporal_metrics.json).

Held out 486 of 972 silver-labelled companies; 702 tags grouped by quarter first seen (357/190/85/70). Q1 is the fit/reference quarter and Q2–Q4 the forward tests. Same learner and score rules as the notebook.

| Quarter | Test tags | Notebook frozen Q1 | Notebook refreshed | Own-company leaky index | Time-restricted frozen Q1 | Time-restricted refreshed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2016q1 | 357 | 64.1% (58.9%–69.1%) | 64.1% (58.9%–69.1%) | 65.0% (59.8%–69.9%) | 63.3% (58.1%–68.3%) | 63.3% (58.1%–68.3%) |
| 2016q2 | 190 | 60.5% (53.2%–67.5%) | 58.4% (51.1%–65.5%) | 73.7% (66.8%–79.8%) | 59.5% (52.1%–66.5%) | 58.4% (51.1%–65.5%) |
| 2016q3 | 85 | 61.2% (50.0%–71.6%) | 62.4% (51.2%–72.6%) | 70.6% (59.7%–80.0%) | 61.2% (50.0%–71.6%) | 62.4% (51.2%–72.6%) |
| 2016q4 | 70 | 52.9% (40.6%–64.9%) | 52.9% (40.6%–64.9%) | 75.7% (64.0%–85.2%) | 51.4% (39.2%–63.6%) | 52.9% (40.6%–64.9%) |

Frozen keeps the Q1 index; refreshed adds available later-quarter references. Test companies stay out of the honest index. The deliberately leaky comparator includes their own Q1 examples and must not be treated as the service benchmark.

The notebook diagnostic fits its text vocabulary from the full year. The separate restricted-input refits use only line items/vocabulary and taxonomy metadata available by cutoff. The strict frozen Q1 index achieves 59.5% top-5 in Q2, 61.2% in Q3 and 51.4% in Q4. Intervals are wide and overlap; 70 Q4 tags do not establish a clear refresh benefit.

The original diagnostic matches Nathan's notebook table (Q2 frozen 60.5%); notebook narrative elsewhere quotes 60.0%. Use the measured table and disclose that narrative discrepancy. Silver references/cohort and hand concept choices remain retrospective; this is not a fully prospectively frozen 2016 deployment, and neither experiment proves future-year performance. The strict refit is an input sensitivity check, not a replacement champion.

The refreshed comparison uses data through the end of the tested quarter, including other companies' filings from that quarter. It is not a beginning-of-quarter deployment or an exact as-of-filing-date simulation. The frozen Q1 model is the forward-cutoff test for Q2–Q4.

Company exclusion applies to the retrieval index and statement eligibility, preserving the given implementation. The vocabulary still uses standard-line text from all companies visible by the cutoff, including held-out companies. The stricter run restricts time exposure; it is not a newly designed fully inductive company-split learner.
