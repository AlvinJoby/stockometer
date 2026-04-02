# Stockometer

Small Flask app for stock analysis charts and summary metrics.

## Features

- Historical stock analysis charts and summary metrics
- Ticker autocomplete suggestions on the landing page while typing

## Local setup

1. Create a virtual environment:
   `python3 -m venv .venv`
2. Activate it:
   `source .venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start the app:
   `python app.py`
5. Open:
   `http://127.0.0.1:5000`

## Run tests

`python -m unittest discover -s tests -v`

## Notes

- The app fetches market data live through `yfinance`, so an internet connection is required while using it.
- Ticker suggestions also use Yahoo Finance search through `yfinance.Search`.
- This repo targets Python 3.9+.
