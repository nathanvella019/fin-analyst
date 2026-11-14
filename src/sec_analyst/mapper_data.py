"""Prepare the given mapper's input tables."""

from pathlib import Path

import duckdb
import pandas as pd


def prepare_line_items(
    connection: duckdb.DuckDBPyConnection,
    processed_dir: Path,
) -> None:
    """Prepare and cache the notebook's statement line items."""
    connection.execute(
        r"""
        CREATE OR REPLACE MACRO norm_label(s) AS
        trim(
            regexp_replace(
                regexp_replace(
                    lower(coalesce(s, '')),
                    '[^a-z, ]', ' ', 'g'
                ),
                '\s+', ' ', 'g'
            )
        )
        """
    )

    processed_dir.mkdir(parents=True, exist_ok=True)
    path = processed_dir / "08_line_items.parquet"
    path_sql = str(path).replace("'", "''")

    query = """
        SELECT
            p.adsh,
            s.cik,
            s.fsq,
            p.tag,
            any_value(p.custom) AS custom,
            arg_min(p.stmt, p.report::INT * 1000 + p.line) AS stmt,
            norm_label(
                arg_min(p.plabel, p.report::INT * 1000 + p.line)
            ) AS label
        FROM pre p
        JOIN sub s USING (adsh)
        WHERE p.inpth = 0
          AND p.stmt IN ('BS', 'IS', 'CF', 'EQ', 'CI')
        GROUP BY p.adsh, s.cik, s.fsq, p.tag
    """

    if not path.exists():
        connection.execute(
            f"COPY ({query}) TO '{path_sql}' "
            "(FORMAT parquet, COMPRESSION zstd)"
        )

    connection.execute(
        "CREATE OR REPLACE TABLE line_items AS "
        f"SELECT * FROM read_parquet('{path_sql}')"
    )
    connection.execute(
        "CREATE OR REPLACE VIEW li AS SELECT * FROM line_items"
    )


def prepare_silver_labels(
    connection: duckdb.DuckDBPyConnection,
    processed_dir: Path,
    min_abs_usd: int,
) -> pd.DataFrame:
    """Prepare the notebook's inferred custom-to-standard matches."""
    processed_dir.mkdir(parents=True, exist_ok=True)
    path = processed_dir / "08_silver.parquet"
    path_sql = str(path).replace("'", "''")

    query = f"""
        WITH cf AS (
            SELECT l.cik, n.adsh, n.tag, l.stmt,
                   n.ddate, n.qtrs, n.value
            FROM num n
            JOIN li l USING (adsh, tag)
            WHERE n.custom
              AND n.coreg IS NULL
              AND n.uom = 'USD'
              AND abs(n.value) >= {min_abs_usd}
        ),
        sf AS (
            SELECT s.cik, n.adsh, n.tag, n.ddate, n.qtrs, n.value
            FROM num n
            JOIN sub s USING (adsh)
            WHERE NOT n.custom
              AND n.coreg IS NULL
              AND n.uom = 'USD'
              AND abs(n.value) >= {min_abs_usd}
              AND (s.cik, n.ddate, n.qtrs, n.value) IN (
                  SELECT (cik, ddate, qtrs, value) FROM cf
              )
        ),
        pairs AS (
            SELECT c.cik, c.adsh, c.tag AS ctag,
                   f.tag AS stag, c.ddate, c.qtrs
            FROM cf c
            JOIN sf f
              ON c.cik = f.cik
             AND c.ddate = f.ddate
             AND c.qtrs = f.qtrs
             AND c.value = f.value
             AND c.adsh <> f.adsh
            JOIN li l
              ON l.adsh = f.adsh
             AND l.tag = f.tag
             AND l.stmt = c.stmt
        ),
        clean AS (
            SELECT p.*
            FROM pairs p
            ANTI JOIN li x
              ON x.adsh = p.adsh AND x.tag = p.stag
        ),
        cand AS (
            SELECT cik, ctag, stag,
                   count(DISTINCT (ddate, qtrs)) AS n_ctx
            FROM clean
            GROUP BY ALL
        )
        SELECT cik, ctag, any_value(stag) AS stag,
               max(n_ctx) AS n_ctx
        FROM cand
        GROUP BY cik, ctag
        HAVING count(*) = 1
    """

    if not path.exists():
        connection.execute(
            f"COPY ({query}) TO '{path_sql}' "
            "(FORMAT parquet, COMPRESSION zstd)"
        )

    connection.execute(
        "CREATE OR REPLACE TABLE silver AS "
        f"SELECT * FROM read_parquet('{path_sql}')"
    )

    return connection.execute("""
        SELECT s.*, l.label, l.stmt, l.fsq
        FROM silver s
        JOIN (
            SELECT cik, tag,
                   arg_min(label, fsq) AS label,
                   arg_min(stmt, fsq) AS stmt,
                   min(fsq) AS fsq
            FROM li
            WHERE custom
            GROUP BY 1, 2
        ) l
          ON l.cik = s.cik AND l.tag = s.ctag
    """).df()
