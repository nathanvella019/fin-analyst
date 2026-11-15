# Thin notebook check — 15 November 2026

`notebooks/analyst_client.ipynb` was added in tested source revision `7552b91`. It contains four code cells: package/config imports, warehouse/concept inspection, calls to the five packaged accounting checks, and a packaged R4 question/SQL-verification example. No separate learner or copied SQL-template implementation lives in the notebook.

Executed all four code cells sequentially using the project Python environment. Birner candidate matched USD 63,843,837 and the SQL recomputation. Identity checks run through package functions. The original parent notebook remains unchanged. This verifies cell execution, not a Jupyter UI or kernel-selection workflow. Repeat with `python3 scripts/verify_notebook.py`; detailed stdout and notebook SHA-256 are saved in ignored `data/evaluation/notebook_client_check.json`.

VS Code users should select the project `.venv` kernel and run the notebook from the repository root or its `notebooks/` folder. The package must be installed and data prepared first. The notebook is read-oriented and does not download data. Its example is explicitly a review candidate.
