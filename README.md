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
- `requests` + `BeautifulSoup` for HTML parsing
- `playwright` (optional) for JS-rendered pages
- Structured logging via the standard library `logging`

## Roadmap

- [ ] Scraping logic for capacity tables
- [ ] CSV / JSON export
- [ ] Retry logic with exponential backoff
- [ ] Structured logging
- [ ] Basic CLI with `argparse`
- [ ] Unit tests on parsing layer

## Scope and disclaimer

This repository is a **personal exercise** built from scratch on **100% public
data** sourced from the Snam public portal. It contains no proprietary code,
client data, or material from any employer or third party.

## Author

Andrea Rovea — [LinkedIn](https://www.linkedin.com/in/andrea-rovea)

## License

MIT — see `LICENSE` file.
