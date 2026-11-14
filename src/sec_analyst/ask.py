"""Ask a financial question using the packaged parser and SQL templates."""

import argparse
import json
from pathlib import Path

import yaml

from sec_analyst.custom_map import prepare_custom_map
from sec_analyst.mapper_data import prepare_line_items
from sec_analyst.service import QuestionService
from sec_analyst.warehouse import connect_warehouse


def main() -> None:
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("question", help="A question about the SEC filings")
    arguments.add_argument(
        "--rung",
        type=int,
        choices=range(5),
        default=4,
        help="Notebook rule level 0–4, default 4 including custom-tag mapping",
    )
    args = arguments.parse_args()

    with Path("config/config.yaml").open(encoding="utf-8") as file:
        settings = yaml.safe_load(file)

    with connect_warehouse(
        Path(settings["processed_dir"]), settings["quarters"]
    ) as connection:
        service = QuestionService(connection)
        if args.rung == 4:
            parsed = service.parser.parse(args.question)
            if parsed["status"] == "ok" and "ciks" in parsed:
                prepare_line_items(connection, Path(settings["processed_dir"]))
                prepare_custom_map(connection, parsed["ciks"])
        result = service.answer(args.question, args.rung)
        if result["status"] == "answered":
            result["verification"] = service.verify(result["sql"], result["value"])
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
