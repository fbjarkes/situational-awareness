"""Market data providers and the symbols each one can supply.

TradingView symbols are exchange-qualified (``NYSE:NEM``, ``INDEX:MMOH``).
Alpaca symbols are plain US tickers (``NEM``). Alpaca market data covers
US-listed stocks and ETFs only, so TradingView breadth indices and foreign
listings have no Alpaca equivalent.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PROVIDERS = {"tradingview": "TradingView", "alpaca": "Alpaca"}

# TradingView exchange prefixes for US listings that Alpaca also carries.
US_EXCHANGES = {"NYSE", "NASDAQ", "AMEX", "ARCA", "NYSEARCA", "BATS", "CBOE"}
ALPACA_DATA_URL = "https://data.alpaca.markets"
ALPACA_FEEDS = ("iex", "sip")
ALPACA_ADJUSTMENTS = ("raw", "split", "dividend", "all")


def provider_label(provider: str) -> str:
    return PROVIDERS.get(provider, provider)


def alpaca_symbol(symbol: str) -> str | None:
    """Return the Alpaca ticker for a symbol, or None if Alpaca cannot supply it."""
    if ":" in symbol:
        exchange, ticker = symbol.split(":", 1)
        return ticker if exchange.upper() in US_EXCHANGES else None
    # Bare labels with a market suffix (e.g. "NST AU") are foreign listings.
    if " " in symbol.strip() or not symbol.strip():
        return None
    return symbol.strip()


def alpaca_unavailable_reason(symbol: str) -> str:
    if symbol.upper().startswith("INDEX:"):
        return "TradingView index; Alpaca does not publish breadth indices."
    return "Not a US listing; Alpaca market data covers US-listed stocks and ETFs only."


def alpaca_credentials() -> dict:
    key, secret = os.environ.get("APCA_API_KEY_ID"), os.environ.get("APCA_API_SECRET_KEY")
    if not key or not secret:
        raise ValueError("Alpaca requires APCA_API_KEY_ID and APCA_API_SECRET_KEY in the environment")
    return {"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret}


def fetch_alpaca_daily(symbols, start: date, end: date | None = None, *, feed: str = "iex",
                       adjustment: str = "split", base_url: str | None = None,
                       opener=urlopen) -> dict:
    """Fetch daily bars for Alpaca tickers in the bar-store payload shape.

    Bars are keyed by Alpaca ticker. Daily bar timestamps are New York
    midnight, so the UTC date of ``t`` is the session date.
    """
    if feed not in ALPACA_FEEDS:
        raise ValueError(f"Unsupported Alpaca feed: {feed}")
    if adjustment not in ALPACA_ADJUSTMENTS:
        raise ValueError(f"Unsupported Alpaca adjustment: {adjustment}")
    symbols = list(dict.fromkeys(symbols))
    if not symbols:
        raise ValueError("At least one Alpaca symbol is required")
    headers = alpaca_credentials()
    url = (base_url or os.environ.get("APCA_DATA_URL") or ALPACA_DATA_URL).rstrip("/") + "/v2/stocks/bars"
    series = {s: {} for s in symbols}
    # Alpaca limits the URL and the page size; request in modest groups.
    for i in range(0, len(symbols), 50):
        group = symbols[i:i + 50]
        token = None
        while True:
            query = {"symbols": ",".join(group), "timeframe": "1Day", "start": start.isoformat(),
                     "limit": 10000, "adjustment": adjustment, "feed": feed, "sort": "asc"}
            if end:
                query["end"] = end.isoformat()
            if token:
                query["page_token"] = token
            with opener(Request(f"{url}?{urlencode(query)}", headers=headers), timeout=60) as response:
                page = json.loads(response.read())
            for symbol, bars in (page.get("bars") or {}).items():
                for bar in bars:
                    t = int(datetime.fromisoformat(bar["t"].replace("Z", "+00:00")).timestamp())
                    series[symbol][t] = {"t": t, "o": bar["o"], "h": bar["h"], "l": bar["l"],
                                         "c": bar["c"], "v": bar["v"]}
            token = page.get("next_page_token")
            if not token:
                break
    empty = [s for s, bars in series.items() if not bars]
    return {"schema_version": 1, "provider": "alpaca",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "feed": feed, "adjustment": adjustment,
            "session_timezones": {s: "America/New_York" for s in symbols if series[s]},
            "series": {s: [bars[t] for t in sorted(bars)] for s, bars in series.items() if bars},
            "empty_symbols": empty}
