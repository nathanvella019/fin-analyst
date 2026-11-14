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
