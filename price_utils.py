"""Symbol-based convenience functions over archived daily bars."""
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from bar_store import ROOT, load_bars
from price_stats import lowest_close_period


def lowest_close(symbol: str, period: int | None = None, *, data_root: Path = ROOT,
                 download_date: str | None = None, as_of: date | str | None = None,
                 provider: str = "tradingview") -> int:
    """Return the latest strict N-session closing-low span, including today.

    Reads a stored daily history; never downloads. Equal or higher than the
    preceding close returns 0. A strict low across 365 closes returns 365.
    The result is capped by both `period` and the number of available closes.
    """
    if isinstance(as_of, str):
        as_of = date.fromisoformat(as_of)
    payload = load_bars([symbol], data_root, download_date=download_date, provider=provider)
    prices = {}
    for bar in payload["series"][symbol]:
        observed = (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=bar["t"])).date()
        if (as_of is None or observed <= as_of) and bar.get("c") is not None:
            prices[observed] = bar["c"]
    if not prices:
        raise ValueError(f"No closes for {symbol} on or before {as_of}")
    return lowest_close_period([prices[d] for d in sorted(prices)], period)
