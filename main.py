"""
Entry point for the Stock Data Visualization project.
Prompts the user for input, fetches data from Alpha Vantage, and opens a chart.
"""

from getpass import getpass
import os
from av_client import fetch_series, SERIES_OPTIONS, get_api_key
from charting import make_chart, filter_by_date
from utils import validate_range, norm_symbol, InputError

def pick(prompt: str, options: dict) -> str:
    print(prompt)
    for key, (func, label) in options.items():
        print(f"  {key}) {func.replace('TIME_SERIES_', '').title()}  [{label}]")
    choice = input("Select option number: ").strip()
    if choice not in options:
        raise InputError("Invalid selection.")
    return choice

def pick_chart_type() -> str:
    print("Chart Types:")
    print("  1) Line")
    print("  2) Area")
    print("  3) Candlestick")
    m = {"1": "line", "2": "area", "3": "candlestick"}
    choice = input("Select option number: ").strip()
    if choice not in m:
        raise InputError("Invalid selection.")
    return m[choice]

def ensure_api_key():
    if not get_api_key():
        print("No ALPHAVANTAGE_API_KEY environment variable found.")
        key = getpass("Enter your Alpha Vantage API key (input hidden): ").strip()
        if not key:
            raise InputError("API key is required.")
        os.environ["ALPHAVANTAGE_API_KEY"] = key

def main():
    try:
        ensure_api_key()
        symbol = norm_symbol(input("Enter stock symbol (e.g., AAPL): "))
        series_choice = pick("Time Series Functions:", SERIES_OPTIONS)
        chart_type = pick_chart_type()
        begin = input("Enter begin date (YYYY-MM-DD): ").strip()
        end = input("Enter end date   (YYYY-MM-DD): ").strip()
        b, e = validate_range(begin, end)

        print("Fetching data from Alpha Vantage...")
        df = fetch_series(symbol, series_choice, full=True)
        df_filtered = filter_by_date(df, b, e)

        if df_filtered.empty:
            raise RuntimeError("No data found in the selected date range. Try a different range.")

        print(f"Generating {chart_type} chart...")
        out = make_chart(df_filtered, chart_type, symbol, b, e)
        print(f"Done. Chart opened in your browser: {out}")

    except InputError as ie:
        print(f"[Input error] {ie}")
    except Exception as ex:
        print(f"[Error] {ex}")

if __name__ == "__main__":
    main()
