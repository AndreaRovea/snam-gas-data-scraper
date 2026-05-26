"""Runtime configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_USER_AGENT = (
    "snam-gas-data-scraper/0.1 "
    "(+https://github.com/AndreaRovea/snam-gas-data-scraper)"
)


@dataclass(frozen=True)
class Settings:
    base_url: str
    user_agent: str
    timeout_seconds: float
    log_level: str


def load_settings() -> Settings:
    return Settings(
        base_url=os.getenv("SNAM_BASE_URL", "https://www.snam.it").rstrip("/"),
        user_agent=os.getenv("SCRAPER_USER_AGENT", DEFAULT_USER_AGENT),
        timeout_seconds=float(os.getenv("SCRAPER_TIMEOUT_SECONDS", "15")),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
