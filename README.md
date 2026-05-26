# Snam Gas Data Scraper

> Automation tool to extract public gas transport data from the Snam portal
> (capacity, delivery dates, redelivery points) and save it as structured CSV/JSON.

## Status

🚧 **Work in progress** — codebase is being cleaned and published in stages.
Original prototype developed during my internship at dazerolab (April–May 2026).

## Tech Stack

- Python 3.11+
- `requests` + `BeautifulSoup` for HTML parsing
- `playwright` (optional) for JS-rendered pages
- Structured logging via `logging` standard library

## Roadmap

- [ ] Scraping logic for capacity tables
- [ ] CSV / JSON export
- [ ] Retry logic with exponential backoff
- [ ] Structured logging
- [ ] Basic CLI with `argparse`
- [ ] Unit tests on parsing layer

## Author

Andrea Rovea
LinkedIn: [andrea-rovea](https://www.linkedin.com/in/andrea-rovea)

## License

MIT — see `LICENSE` file.

