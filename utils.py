from datetime import datetime
from typing import Tuple

DATE_FMT = "%Y-%m-%d"

class InputError(Exception):
    pass

def parse_date(s: str) -> datetime.date:
    try:
        return datetime.strptime(s.strip(), DATE_FMT).date()
    except ValueError:
        raise InputError(f"Date '{s}' must be in YYYY-MM-DD format.")

def validate_range(begin_s: str, end_s: str) -> Tuple[datetime.date, datetime.date]:
    b = parse_date(begin_s)
    e = parse_date(end_s)
    if e < b:
        raise InputError("End date cannot be before begin date.")
    return b, e

def norm_symbol(sym: str) -> str:
    s = sym.strip().upper()
    if not s or any(ch.isspace() for ch in s):
        raise InputError("Stock symbol cannot be empty or contain whitespace.")
    return s
