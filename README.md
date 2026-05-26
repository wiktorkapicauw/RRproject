# Volatility Forecasting with GARCH Models

Reproducible pipeline for forecasting Netflix (NFLX) stock volatility
using GARCH, GJR-GARCH and EGARCH models.

## Team

- Oleg Fyłypczuk
- Maciej Głowacki
- Wiktor Kapica

## Quick Start (Docker Hub)

Pull the image and generate the report (~3 min):

```bash
docker pull wiktorkapicauw/rrproject:latest
mkdir -p output
docker run --rm -v "$(pwd)/output:/app/output" wiktorkapicauw/rrproject:latest
```

Open `output/report.html` in a browser.

## Build Locally

```bash
git clone https://github.com/wiktorkapicauw/RRproject.git
cd RRproject
docker compose build
docker compose run --rm app
```

The generated report is saved to `output/report.html`.

## Project Structure

```
src/volatility_forecasting/
├── data.py            # DataLoader — Yahoo Finance download, log returns
├── models.py          # VolatilityModel — GARCH / GJR-GARCH / EGARCH
├── forecasting.py     # RollingForecaster — rolling out-of-sample forecast
└── plots.py           # Matplotlib visualisation functions
report.qmd             # Quarto report (literate programming)
Dockerfile             # Reproducible environment with Python 3.12 + Quarto
docker-compose.yml
Makefile
pyproject.toml
```

## Methodology

- **Version control** — Git + GitHub (feature branches, pull requests)
- **Environment** — Docker (Python 3.12-slim, Quarto 1.9)
- **Code quality** — black, isort, flake8, pre-commit hooks
- **Report** — Quarto (literate programming, self-contained HTML)

## AI Disclosure

LLM assistance (Claude, Anthropic) was used for code scaffolding
and report structure. All outputs were reviewed and adapted by the team.
