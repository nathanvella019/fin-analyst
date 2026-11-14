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

Nathan successfully installed `fin-analyst` version `0.1.0` in editable mode and confirmed that importing `sec_analyst` resolves to `src/sec_analyst/__init__.py`. The package setup is ready for review and a Git commit. Extracting the loader is the next implementation step.

## Working folders

- `src/sec_analyst/` holds the Python code, imported as `sec_analyst`.
- `config/` holds project settings.
- `tests/` holds checks for the code and data rules.
- `notebooks/` holds notebook clients for the package.
- `docs/decisions/` holds short records of project decisions.
- `docs/diary/entry-1/` holds the first diary's evidence and submission materials.

Our collaboration notes and detailed progress are recorded in the parent `README.md`.
