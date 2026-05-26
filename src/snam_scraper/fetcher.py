"""HTTP client with retry/backoff for fetching pages from the Snam public portal."""

from __future__ import annotations

import logging

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .config import Settings, load_settings

logger = logging.getLogger(__name__)


class FetchError(RuntimeError):
    """Raised when a page cannot be retrieved after all retries."""


class Fetcher:
    """Thin wrapper around `requests.Session` with structured retry policy."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or load_settings()
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": self._settings.user_agent})

    @retry(
        retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def get(self, path_or_url: str) -> str:
        url = self._absolute_url(path_or_url)
        logger.info("GET %s", url)
        # ConnectionError/Timeout are left to tenacity for retry; other request
        # errors and non-2xx statuses are surfaced as FetchError.
        response = self._session.get(url, timeout=self._settings.timeout_seconds)
        if response.status_code >= 400:
            raise FetchError(
                f"unexpected status {response.status_code} fetching {url}"
            )
        return response.text

    def _absolute_url(self, path_or_url: str) -> str:
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        return f"{self._settings.base_url}/{path_or_url.lstrip('/')}"

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> Fetcher:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
