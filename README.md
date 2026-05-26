# Snam Gas Data Scraper

> Personal portfolio project — a small automation tool that navigates the public
> Snam portal and extracts structured data on gas transport (capacity, delivery
> dates, redelivery points) into CSV / JSON.

## Status

🚧 **Work in progress** — codebase is being written and published in incremental
stages as a personal learning exercise on **publicly available data only**.
Inspired by my interest in RPA and process automation developed during a recent
professional experience.

## Tech Stack

- Python 3.11+
- `requests` + `BeautifulSoup` (lxml backend) for HTML parsing
- `tenacity` for retry/backoff on transient network errors
- `python-dotenv` for runtime configuration via environment variables
- Structured logging via the standard library `logging`
- `pytest` + `ruff` + `mypy` for tests, linting and type checking

## Project structure

```
snam-gas-data-scraper/
├── pyproject.toml          packaging + tooling config (PEP 621)
├── requirements.txt        runtime dependencies (pinned floors)
├── requirements-dev.txt    + dev tools (pytest, ruff, mypy)
├── Makefile                shortcut targets (install, test, lint, run)
├── .env.example            template for runtime configuration
├── src/snam_scraper/
│   ├── config.py           settings loader (env vars + dotenv)
│   ├── fetcher.py          HTTP client with retry/backoff
│   ├── parser.py           BeautifulSoup-based parsing scaffolding
│   ├── exporter.py         CSV / JSON writers
│   └── cli.py              `argparse`-based entry point
└── tests/
    └── test_fetcher.py     unit tests for the HTTP layer
```

## Getting started

Requires **Python 3.11+** (developed against 3.12).

```bash
# clone
git clone https://github.com/AndreaRovea/snam-gas-data-scraper.git
cd snam-gas-data-scraper

# create a virtual environment and install everything
python3 -m venv .venv
make install

# (optional) configure runtime via .env
cp .env.example .env

# run the CLI
make run
# or directly:
.venv/bin/snam-scraper --url /some/snam/path --output output.csv
```

### Common tasks

```bash
make test         # run pytest with coverage
make lint         # ruff check
make format       # ruff format
make typecheck    # mypy on src/snam_scraper
make clean        # remove caches and build artefacts
```

## Roadmap

- [x] Project scaffolding (packaging, dev tooling)
- [x] HTTP fetcher with retry/backoff
- [x] CLI entry point with `argparse`
- [x] CSV / JSON exporters
- [x] Unit tests on HTTP fetcher
- [ ] Concrete table extractors for the Snam public portal
- [ ] Parser tests on representative HTML fixtures
- [ ] Optional `playwright` support for JS-rendered pages
- [ ] CI workflow (GitHub Actions)

## Known limitations

- The parser layer currently returns generic row records — concrete extractors
  for specific Snam tables will be added incrementally.
- No retry policy is yet applied to 5xx HTTP responses (only to connection /
  timeout errors).
- The `--url` argument accepts either a path (resolved against `SNAM_BASE_URL`)
  or an absolute URL; no smart discovery of pages is implemented.

## Scope and disclaimer

This repository is a **personal exercise** built from scratch on **100% public
data** sourced from the Snam public portal. It contains no proprietary code,
client data, or material from any employer or third party.

## Author

Andrea Rovea — [LinkedIn](https://www.linkedin.com/in/andrea-rovea)

## License

MIT — see `LICENSE` file.
