# Currency Converter

A simple Python GUI application that converts between major world currencies using live exchange rates from the Frankfurter API.

## Features

- Enter an amount to convert
- Choose source and target currencies
- Convert with a single button click
- Swap currencies instantly
- Clear the form
- Validate invalid input such as blank or non-numeric values
- Show the live exchange rate and last update date
- Handle API and network errors gracefully

## Supported Currencies

- USD
- EUR
- JPY
- GBP
- CNY
- AUD
- CAD
- KWD
- KRW
- INR

## Requirements

- Python 3.9 or newer
- Tkinter (usually included with Python)
- requests

## Installation

1. Open a terminal in the project folder.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the App

```bash
python app.py
```

## Run the Tests

```bash
python -m unittest test_app.py
```

## Notes

- The app uses the Frankfurter API, which is free and easy to use.
- The app works on Windows, macOS, and Linux as long as Python and Tkinter are installed.
- If the internet connection is unavailable, the app shows a friendly error message instead of crashing.
