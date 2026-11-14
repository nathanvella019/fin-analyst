"""Prepare the SEC quarters listed in the project configuration."""

from pathlib import Path

import yaml

from sec_analyst.loader import load_quarter


def main() -> None:
    with Path("config/config.yaml").open(encoding="utf-8") as file:
        settings = yaml.safe_load(file)

    raw_dir = Path(settings["raw_dir"])
    processed_dir = Path(settings["processed_dir"])

    for quarter in settings["quarters"]:
        load_quarter(
            quarter=quarter,
            raw_dir=raw_dir,
            processed_dir=processed_dir,
            kaggle_handle=settings["kaggle_handle"],
        )


if __name__ == "__main__":
    main()