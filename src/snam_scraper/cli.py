"""Command-line interface for the Snam gas data scraper."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .config import load_settings
from .exporter import write_csv, write_json
from .fetcher import Fetcher, FetchError
from .parser import parse_records

logger = logging.getLogger("snam_scraper")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="snam-scraper",
        description="Fetch and parse public gas transport data from the Snam portal.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--url",
        required=True,
        help="Page path or absolute URL to fetch from the Snam public portal.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output file path. Format inferred from extension (.csv or .json).",
    )
    return parser


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s — %(message)s",
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = load_settings()
    _configure_logging(settings.log_level)

    try:
        with Fetcher(settings) as fetcher:
            html = fetcher.get(args.url)
    except FetchError as exc:
        logger.error("fetch failed: %s", exc)
        return 1

    records = parse_records(html)
    logger.info("extracted %d records", len(records))

    suffix = args.output.suffix.lower()
    if suffix == ".csv":
        write_csv(records, args.output)
    elif suffix == ".json":
        write_json(records, args.output)
    else:
        logger.error("unsupported output format: %s (use .csv or .json)", suffix)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
