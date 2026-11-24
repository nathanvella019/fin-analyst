# Model card · SEC standard-tag mapper, version 2

**Owner:** Nathan Vella · **Registry:** `models:/sec-standard-tag-mapper/2` · **Training cutoff:** 31 March 2016

## What a research manager can use it for

When a company invents its own accounting tag, an analyst needs to know which standard tag might describe the same thing. This mapper reads the custom tag name, the company's line label and the type of financial statement. It returns five standard tags in ranked order. The supplied TF-IDF method compares words and pairs of words with taxonomy labels and lines used by other filers.

Use the list to narrow a search. The analyst reads the cited statement and checks what the line includes before approving a mapping or releasing a figure. For example, sales of goods can be just one part of total sales. Similar wording alone cannot settle that distinction. The financial-question API requires analyst review. Its answer accuracy is measured separately.

| Question an analyst might ask | Result on 345 later cases |
|---|---:|
| How often was the first suggestion the expected tag? | 115/345 (33.33%) |
| How often did the five suggestions include it? | 201/345 (58.26%), 95% interval 52.66–63.77% |
| How did the simpler method using taxonomy names and labels alone perform? | 150/345 (43.48%) in the first five |

In 144 cases the expected tag was missing from the entire list. An analyst needs a way to reject all five and investigate the filing.

## What a regulator or reviewer can trace

The March build used standard line items from 6,022 eligible SEC filings in January–March 2016. The vocabulary and search index excluded 486 test companies. The frozen forward test used 345 company/tag cases from 278 of those companies first seen in April–December. Later filings sometimes reused the same figure with a standard tag. That let us infer an expected answer for scoring. These matches can be mistaken and cover only cases where later evidence exists.

We resampled whole companies 10,000 times to estimate the interval. The evidence covers the 2016 filing mix and taxonomy. Performance on later taxonomy releases requires fresh evaluation. This version supports company-filing research. Automatic publication of figures and individual credit decisions fall outside its evaluated use.

Training commit `32d16c6`, MLflow training run `433508d40ff64b7a9beff45d995f7f96`, evaluation run `704dd329ca6c47e1a2d2c58caeefeac5`. The registry record contains the full training and holdout fingerprints. [Version evidence](evidence/rd2/registry-results.json) · [Evaluation and intervals](evidence/rd2/task-3-measurement.md)

## What the on-call engineer does

At the end of each filing quarter run `python -m sec_analyst.rd2_monitoring` from the project root. Investigate if the statement-type mix shifts by **at least 10%** from Q1 or quarterly top-five accuracy falls **below 52.66%**. Inspect missing labels, new tags, taxonomy changes and examples of misses. Q4 triggered both reviews at 10.45% drift and 36/70 correct. One low quarter calls for investigation. Two consecutive scored quarters below the floor trigger training a candidate. Nathan decides whether to promote or roll back after checking the evidence and CI. [Monitoring results](evidence/rd2/task-5.md)

**Rollback target:** February, version 1, scored 191/345. For a rehearsal, run the following from the project root with the RD2 environment and local registry. The command loads the models, switches the champion alias to February, compares all 345 ordered lists with February's saved predictions, then restores and verifies March.

```bash
python -m sec_analyst.rd2_registry demo 7544afb5e79542c0907469a0bfda8024 433508d40ff64b7a9beff45d995f7f96 9e9bc1fbf997480ba1be2e4189404a4b
```

For an incident where February must stay selected, Nathan first verifies the retained version 1 against its saved rankings. Using the MLflow client connected to this project's registry, he calls `client.set_registered_model_alias("sec-standard-tag-mapper", "champion", 1)`, reads the alias back and loads `models:/sec-standard-tag-mapper@champion` to check those rankings again. This selects the local registry model. The question API has its own model-loading path. [Tested rollback and registry setup](evidence/rd2/task-4.md)
