"""HTML parsing layer — extracts structured records from fetched pages.

The current implementation provides only a generic scaffold. Concrete extractors
for specific Snam tables (capacity, redelivery points, delivery dates) will be
added incrementally — see the roadmap in README.md.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GasTransportRecord:
    """Single row of public gas transport data.

    Fields are intentionally optional during the work-in-progress phase: as the
    scraper is taught to recognise more table layouts, more fields will become
    mandatory.
    """

    redelivery_point: str | None = None
    capacity_value: float | None = None
    capacity_unit: str | None = None
    delivery_date: str | None = None


def parse_records(html: str) -> list[GasTransportRecord]:
    """Parse an HTML page and return a list of records.

    Returns an empty list when no rows are matched. The parser is intentionally
    permissive at this stage and will be tightened to match specific portal
    layouts in upcoming iterations.
    """
    soup = BeautifulSoup(html, "lxml")
    records: list[GasTransportRecord] = []

    for row in soup.select("table tr"):
        cells = [cell.get_text(strip=True) for cell in row.select("td")]
        if not cells:
            continue
        records.append(GasTransportRecord(redelivery_point=cells[0] or None))

    logger.debug("parsed %d records", len(records))
    return records
