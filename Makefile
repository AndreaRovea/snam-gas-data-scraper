.PHONY: install test lint typecheck run clean help

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
PYTEST := .venv/bin/pytest
RUFF := .venv/bin/ruff
MYPY := .venv/bin/mypy

help:
	@echo "Targets:"
	@echo "  install     install runtime + dev dependencies inside .venv"
	@echo "  test        run pytest with coverage"
	@echo "  lint        run ruff linter"
	@echo "  format      run ruff formatter"
	@echo "  typecheck   run mypy static type checker"
	@echo "  run         run the CLI (snam-scraper --help)"
	@echo "  clean       remove caches and build artifacts"

install:
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

test:
	$(PYTEST) --cov=snam_scraper --cov-report=term-missing

lint:
	$(RUFF) check src tests

format:
	$(RUFF) format src tests

typecheck:
	$(MYPY)

run:
	$(PYTHON) -m snam_scraper.cli --help

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
