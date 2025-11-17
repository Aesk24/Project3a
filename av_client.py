import os
import time
from typing import Dict, Tuple
import requests
import pandas as pd

API_URL = "https://www.alphavantage.co/query"

# Mapping friendly names to Alpha Vantage functions and default key in JSON
SERIES_OPTIONS = {
    "1": ("TIME_SERIES_DAILY", "Time Series (Daily)"),
    "2": ("TIME_SERIES_DAILY_ADJUSTED", "Time Series (Daily)"),
    "3": ("TIME_SERIES_WEEKLY", "Weekly Time Series"),
    "4": ("TIME_SERIES_MONTHLY", "Monthly Time Series")
}

def get_api_key() -> str:
    key = os.getenv("ALPHAVANTAGE_API_KEY")
    return key

def fetch_series(symbol: str, series_key: str, full: bool = True) -> pd.DataFrame:
    """Fetch a time series and return a pandas DataFrame with a Date index."""
    if series_key not in SERIES_OPTIONS:
        raise ValueError("Invalid series selection.")
    func, json_key = SERIES_OPTIONS[series_key]
    params = {
        "function": func,
        "symbol": symbol,
        "apikey": get_api_key() or "",
    }
    # full history for daily endpoints (compact ~100 points)
    if func.startswith("TIME_SERIES_DAILY"):
        params["outputsize"] = "full" if full else "compact"

    resp = requests.get(API_URL, params=params, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP error {resp.status_code}: {resp.text[:200]}")

    data = resp.json()
    if "Note" in data and "frequency" in data["Note"].lower():
        # Rate limit note from Alpha Vantage
        raise RuntimeError("Rate limit hit. Please wait a minute and retry.")

    if json_key not in data:
        # Provide helpful diagnostics
        msg = data.get("Error Message") or data.get("Note") or str(data)[:300]
        raise RuntimeError(f"Unexpected API response; check symbol or API key. Details: {msg}")

    ts: Dict[str, Dict[str, str]] = data[json_key]
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(ts, orient="index").sort_index()
    # Normalize column names
    rename_map = {
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. adjusted close": "adjusted_close",
        "5. volume": "volume",
        "6. volume": "volume",
        "6. dividend amount": "dividend",
        "7. dividend amount": "dividend",
        "7. split coefficient": "split_coefficient",
        "8. split coefficient": "split_coefficient",
    }
    df = df.rename(columns=rename_map)
    # Ensure numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.index.name = "date"
    df.reset_index(inplace=True)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df
