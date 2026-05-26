"""Unit tests for the HTTP fetcher."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from snam_scraper.config import Settings
from snam_scraper.fetcher import Fetcher, FetchError


def _settings(base_url: str = "https://example.com") -> Settings:
    return Settings(
        base_url=base_url,
        user_agent="test-agent/1.0",
        timeout_seconds=1.0,
        log_level="WARNING",
    )


def test_get_returns_body_on_success() -> None:
    fake_response = MagicMock(status_code=200, text="<html>ok</html>")
    with (
        patch("requests.Session.get", return_value=fake_response) as mocked,
        Fetcher(_settings()) as fetcher,
    ):
        body = fetcher.get("/some/path")
    assert body == "<html>ok</html>"
    mocked.assert_called_once()
    called_url = mocked.call_args.args[0]
    assert called_url == "https://example.com/some/path"


def test_get_raises_on_http_error() -> None:
    fake_response = MagicMock(status_code=500, text="boom")
    with (
        patch("requests.Session.get", return_value=fake_response),
        Fetcher(_settings()) as fetcher,
        pytest.raises(FetchError),
    ):
        fetcher.get("/x")


def test_get_accepts_absolute_url() -> None:
    fake_response = MagicMock(status_code=200, text="ok")
    with (
        patch("requests.Session.get", return_value=fake_response) as mocked,
        Fetcher(_settings("https://example.com")) as fetcher,
    ):
        fetcher.get("https://other.example.org/full")
    called_url = mocked.call_args.args[0]
    assert called_url == "https://other.example.org/full"


def test_get_raises_after_retries_on_connection_error() -> None:
    with (
        patch("requests.Session.get", side_effect=requests.ConnectionError("nope")),
        Fetcher(_settings()) as fetcher,
        pytest.raises(requests.ConnectionError),
    ):
        fetcher.get("/x")
