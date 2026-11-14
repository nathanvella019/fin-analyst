"""Apply the notebook's mapper to selected companies' custom tags."""

import duckdb
import numpy as np
import pandas as pd

from sec_analyst.mapper import TagMapper


def prepare_custom_map(
    connection: duckdb.DuckDBPyConnection,
    company_ciks: list[int],
    mapper: TagMapper | None = None,
) -> pd.DataFrame:
    """Create the notebook's custom_map table for the requested companies."""
    company_ids = ",".join(str(int(cik)) for cik in company_ciks)
    company_filter = f"cik IN ({company_ids})" if company_ids else "FALSE"
    custom_items = connection.execute(f"""
        SELECT adsh, tag AS ctag, label, stmt
        FROM li
        WHERE custom AND stmt = 'IS' AND {company_filter}
    """).df()

    if custom_items.empty:
        custom_items["stag"] = pd.Series(dtype="str")
        custom_items["score"] = pd.Series(dtype=np.float32)
    else:
        mapper = mapper if mapper is not None else TagMapper(connection)
        suggestions, scores = mapper.suggest(custom_items, k=1)
        custom_items["stag"] = [suggestion[0] for suggestion in suggestions]
        custom_items["score"] = scores[:, 0]

    connection.register("custom_map_df", custom_items)
    connection.execute("""
        CREATE OR REPLACE TABLE custom_map AS
        SELECT * FROM custom_map_df
    """)
    connection.unregister("custom_map_df")
    return custom_items
