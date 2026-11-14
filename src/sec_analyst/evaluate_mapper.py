"""Run the notebook's company-held-out mapper evaluation."""

from pathlib import Path
import time

import numpy as np
import yaml

from sec_analyst.mapper import TagMapper, ci95, evaluate
from sec_analyst.mapper_data import prepare_line_items, prepare_silver_labels
from sec_analyst.warehouse import connect_warehouse


def main() -> None:
    with Path("config/config.yaml").open(encoding="utf-8") as file:
        settings = yaml.safe_load(file)

    processed_dir = Path(settings["processed_dir"])
    with connect_warehouse(processed_dir, settings["quarters"]) as connection:
        prepare_line_items(connection, processed_dir)
        silver = prepare_silver_labels(
            connection, processed_dir, settings["min_abs_usd"]
        )
        rng = np.random.default_rng(settings["seed"])
        companies = np.array(sorted(silver.cik.unique()))
        held_out = set(rng.choice(companies, len(companies) // 2, replace=False))
        test = silver[silver.cik.isin(held_out)].reset_index(drop=True)
        excluded_companies = ",".join(map(str, sorted(held_out)))

        started = time.perf_counter()
        mapper = TagMapper(connection, where=f"cik NOT IN ({excluded_companies})")
        build_seconds = time.perf_counter() - started

        started = time.perf_counter()
        results = evaluate(mapper, test)
        evaluation_seconds = time.perf_counter() - started

        print(f"Held-out companies: {len(held_out):,} of {len(companies):,}")
        print(f"Indexed tag/label pairs: {mapper.n_pairs:,}")
        print(f"Candidate tags: {len(mapper.classes):,}")
        print(results.to_string(formatters={
            "top-1": "{:.1%}".format,
            "top-5": "{:.1%}".format,
            "test tags": "{:,.0f}".format,
        }))
        top5 = results.loc["both (the baseline mapper)", "top-5"]
        lower, upper = ci95(round(top5 * len(test)), len(test))
        print(f"Baseline top-5 95% interval: {lower:.1%}–{upper:.1%}")
        print(f"Mapper build time: {build_seconds:.2f}s")
        print(f"Evaluation time: {evaluation_seconds:.2f}s")


if __name__ == "__main__":
    main()
