"""Connect the prepared SEC tables to DuckDB."""

from pathlib import Path

import duckdb


def connect_warehouse(
    processed_dir: Path,
    quarters: list[str],
) -> duckdb.DuckDBPyConnection:
    """Open a database connection for the selected quarters."""
    connection = duckdb.connect(
        config={"memory_limit": "1GB", "threads": "1"}
    )
    connection.execute("SET enable_progress_bar=false")

    for table in ("sub", "num", "pre", "tag"):
        files = [
            str(processed_dir / f"08_{table}_{quarter}.parquet")
            for quarter in quarters
        ]

        relation = connection.read_parquet(files)

        if table == "sub":
            relation.create(table)
        else:
            relation.create_view(table)

    return connection