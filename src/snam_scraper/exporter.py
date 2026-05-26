"""Persist scraped records to CSV or JSON."""

from __future__ import annotations

import csv
import json
import logging
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from .parser import GasTransportRecord

logger = logging.getLogger(__name__)


def write_csv(records: Sequence[GasTransportRecord], output_path: Path) -> None:
    if not records:
        logger.warning("no records to write to %s", output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(GasTransportRecord.__dataclass_fields__.keys())
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))
    logger.info("wrote %d records to %s", len(records), output_path)


def write_json(records: Sequence[GasTransportRecord], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(record) for record in records]
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    logger.info("wrote %d records to %s", len(records), output_path)
