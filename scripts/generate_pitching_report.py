"""CLI entry point for generating the Kansas City Royals pitching report."""
from __future__ import annotations

import argparse
from pathlib import Path

from pitching_report.report_builder import build_report_from_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a multi-start pitching report.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/report_config.yaml"),
        help="Path to the YAML configuration file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_report_from_file(args.config)


if __name__ == "__main__":
    main()
