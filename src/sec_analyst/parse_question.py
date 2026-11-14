"""Inspect how the given parser interprets a question."""

import argparse
import json
from pathlib import Path

import yaml

from sec_analyst.parser import QuestionParser
from sec_analyst.warehouse import connect_warehouse


def main() -> None:
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("question", help="A question about the SEC filings")
    arguments.add_argument(
        "--raw", action="store_true", help="Use the notebook's raw-schema baseline"
    )
    args = arguments.parse_args()

    with Path("config/config.yaml").open(encoding="utf-8") as file:
        settings = yaml.safe_load(file)

    with connect_warehouse(
        Path(settings["processed_dir"]), settings["quarters"]
    ) as connection:
        parser = QuestionParser(connection)
        result = parser.parse(args.question, kb_context=not args.raw)
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
