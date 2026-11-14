"""Prepare the given mapper's input tables."""

from pathlib import Path

import duckdb


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