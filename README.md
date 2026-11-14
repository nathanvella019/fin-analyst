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
