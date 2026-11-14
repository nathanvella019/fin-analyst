# Financial Statement Analyst

ARI3217 Task 08 turns questions about SEC financial statements into answers with their filing sources. The immediate milestone is Reflective Diary Entry 1, due 23 November 2026.

## Current status

The project repository has been initialised. Implementation begins with extracting the supplied notebook's loader into `src/sec_analyst/`.

Nathan confirmed Docker Desktop works on the Apple silicon Mac by running `hello-world`. Reported versions are Docker 29.9.3 and Docker Compose v5.7.0.

The reference notebook is currently in the parent directory. The existing data is also in the parent directory under `data/`. Installation, configuration and run commands will be documented as they are implemented.

## Python environment

Use Python 3.14.0 and activate the project's virtual environment from the repository root.

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Nathan installed the notebook dependencies and reported successful dependency and import checks in the new environment. `requirements.txt` now records the installed dependency versions for fresh-copy reproduction.

The saved package configuration is in `pyproject.toml`. The Python package is named `sec_analyst`, referring to the SEC filings. Reinstall the editable project after the package rename and check the import.

```bash
python3 -m pip install -e .
python3 -c "import sec_analyst; print(sec_analyst.__file__)"
```

Nathan successfully installed `fin-analyst` version `0.1.0` in editable mode and confirmed that importing `sec_analyst` resolves to `src/sec_analyst/__init__.py`. The package setup is committed as `ec7fdc6`. The next implementation step is extracting the loader.

## Working folders

- `src/sec_analyst/` holds the Python code, imported as `sec_analyst`.
- `config/` holds project settings.
- `tests/` holds checks for the code and data rules.
- `notebooks/` holds notebook clients for the package.
- `docs/decisions/` holds short records of project decisions.
- `docs/diary/entry-1/` holds the first diary's evidence and submission materials.

Our collaboration notes and detailed progress are recorded in the parent `README.md`.

## Loader status

`src/sec_analyst/loader.py` contains `get_raw`, the notebook's streaming `unpack_members`, its exact `TSV` and `EXTRACT` settings, and `load_quarter` with explicit folder arguments. The queries preserve the notebook's column selection and exclusion of contact details. The VS Code KaggleHub import warning was resolved by selecting the project interpreter.

## Quarter conversion

On 14 November 2026, ran `load_quarter` using the project `.venv`, local raw file `../archive (1)/2016q1.json`, and output folder `data/processed/`. The conversion completed successfully:

| Table | Rows |
| --- | ---: |
| sub | 6,535 |
| num | 3,485,997 |
| pre | 1,051,814 |
| tag | 85,458 |

All four Parquet files were opened and counted with DuckDB. The numeric-fact count matches Nathan's notebook baseline. The `sub` column list matches the notebook selection. A repeat call skipped conversion because all four outputs existed. Git confirms the generated data file is ignored. Raw JSON was retained and the temporary directory was cleaned up automatically.

Both existing loader tests passed after adding the conversion function. The Kaggle download branch remains unverified because the raw file was available locally. Nathan subsequently ran Q2–Q4 successfully and reported full-year totals of 27,677 filings, 7,229 distinct companies and 10,890,076 numeric facts, matching the notebook baseline. These totals check dataset size, not every individual value. Next: review the loader changes and create a Git checkpoint, then continue packaging in small explained steps.

## Next guided step: configuration

Confirmed loader checkpoint `6672dc6` (`Extract and verify SEC data loader`) and a clean working tree before this step. Next Nathan will create `config/config.yaml`, as requested by the notebook, starting with the dataset handle, four quarters and local raw/processed paths. These paths initially resolve relative to the repository root. PyYAML is already pinned in `requirements.txt`; no new installation is needed for this step. Nathan created and saved `config/config.yaml`, then successfully read the dataset handle and four-quarter list with `yaml.safe_load`. Both raw and processed folder checks returned `True`. The remaining Section 0 model and evaluation settings will be migrated as their code is packaged.

`src/sec_analyst/prepare.py` now reads the YAML and calls `load_quarter` for each configured quarter. Run it from the repository root with `python3 -m sec_analyst.prepare`. Nathan reported the command worked as expected. PyYAML is declared as a direct dependency in `pyproject.toml`. Next refresh the editable installation metadata, run the existing tests and commit the configuration and command before adding the DuckDB connection code.

### DuckDB connection step

Configuration and preparation command committed as `410707f` (`Add configuration-driven data preparation`). Next Nathan creates `src/sec_analyst/warehouse.py` with `connect_warehouse(processed_dir, quarters)`. Preserve the notebook layout: materialise `sub` as a DuckDB table, expose `num`, `pre`, and `tag` as views over the explicitly selected quarterly files, and use a 1 GB memory limit and one thread. The assistant checked these relation operations against all four local quarters in a temporary in-memory connection and obtained 27,677 filings, 7,229 companies and 10,890,076 facts. Saving the module and running Nathan's import check remain pending.

### Warehouse module verified by Nathan

Nathan saved `src/sec_analyst/warehouse.py` and ran the import and connection check successfully. The available names were `num`, `pre`, `sub` and `tag`; totals were 27,677 filings, 7,229 companies and 10,890,076 numeric facts. The assistant inspected the saved module. Next guided step is extracting Section 3's exact `CONCEPTS` dictionary into `src/sec_analyst/concepts.py` and adding a function to create the notebook's `kb` table. Keep all phrases, tags and their precedence order. Concept-module creation and its 7-concept/24-member check are pending. Warehouse and concept work will need a Git checkpoint after review.

### Concept dictionary extracted and checked

At Nathan's request, copied the complete Section 3 `CONCEPTS` dictionary exactly into `src/sec_analyst/concepts.py`, below the existing imports, stopping before `kb_rows = []`. Added the supplied `register_concepts(connection)` function. An in-memory DuckDB check passed with 7 concepts and 24 member tags. All generated tags, priority positions and period types matched the dictionary; Assets produced `('Assets', 'Assets', 0, 'instant')`. Code and notes are saved locally. Next Nathan can repeat the check, then connect this knowledge table to the warehouse. Warehouse and concept changes still need a Git checkpoint after review.

### Next guided check: concepts with the warehouse

Next Nathan will open the configured warehouse, call `register_concepts` on that same connection, and join `kb` to standard tag definitions in `tag` to inspect member tags and official labels. This is a read-only check of the prepared files using an in-memory knowledge table. Nathan's integrated run is pending. After it passes, review and commit the warehouse and concept modules together.

### Concept and warehouse integration passed

Nathan ran the integrated check successfully. All seven preferred member tags joined to a standard tag definition: Assets, Cash, Equity, Liabilities, NetIncome, OperatingCashFlow and Revenue. This confirms the packaged warehouse and concept registration work together on one DuckDB connection. The query selected priority-zero members and one available taxonomy label per member. It does not evaluate question-answer accuracy. Next run the existing loader tests, review the staged warehouse and concept modules and README, and create a Git checkpoint. No commit has been made by the assistant.

### Accounting identity checks next

Confirmed warehouse and concepts commit `3794b2c` and clean working tree. Next Nathan creates `src/sec_analyst/checks.py` with the notebook's five `IDENTITIES` and `identity_check`, passing the DuckDB connection explicitly. Preserve source filters, context grouping, max-value selection, complete-row filtering and tolerance of the larger of USD 1,000 or 0.5% of the total. Module creation and running its five checks remain pending. Prior notebook results provide comparison targets of 99.96%, 84.19%, 95.64%, 94.98% and 82.65% in identity order.

### Accounting identity extraction and real-data checks passed

At Nathan's request, copied the notebook's complete `IDENTITIES` dictionary and `identity_check` function into `src/sec_analyst/checks.py`, stopping before the display code. Changed the function to receive `connection` explicitly and replaced its `con.execute` call with `connection.execute`. Ran all five checks through the configured warehouse. Counts and displayed percentages matched the prior notebook run: Assets/L&SE 24,895 and 99.96%; SalesRevenueNet/Goods+Services 1,107 and 84.19%; GrossProfit/Revenue-Cost 3,210 and 95.64%; ProfitLoss/NetIncome+NCI 7,292 and 94.98%; L&SE/Liabilities+StockholdersEquity 17,649 and 82.65%. All figures use the notebook tolerance and filters. The 10-K/10-Q form filter excludes /A forms but does not filter `prevrpt`; this preserves the notebook logic. Next review the results with Nathan and save the check module in Git. No new commit was made by the assistant.

### Next guided mapper preparation step

Next Nathan creates `src/sec_analyst/mapper_data.py` with `prepare_line_items(connection, processed_dir)`. It registers the notebook's label-normalisation SQL macro, prepares the exact Section 3 `line_items` query, caches the result as `08_line_items.parquet` and exposes `line_items` and `li` on the connection. This preserves the source cache behaviour for this stage. Creation and execution are pending. The custom company/tag count comparison target is 100,244. The accounting checks remain saved and verified, with their Git checkpoint still pending.

### Mapper line-item preparation passed

Nathan ran `prepare_line_items` through the configured warehouse and reported 100,244 distinct custom company/tag pairs, matching the notebook baseline. His five sample rows included repeated `AmortizationOfOverhaulCosts` rows with the cleaned label `amortization of overhaul costs` and statement `CF`, plus `AssetsNoncurrentExcludingPropertyPlantAndEquipment` with label `total other assets` and statement `BS`. The sample query displays filing/tag rows; the headline count uses distinct company/tag pairs. The assistant inspected the saved module. Next review and commit README, `checks.py` and `mapper_data.py`, then package the notebook's silver-label preparation. No new Git commit was made by the assistant.
