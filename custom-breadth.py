"""Calculate custom breadth from archived per-symbol daily bars."""
import argparse
import asyncio
from datetime import date, datetime, timedelta, timezone
import json
import hashlib
from pathlib import Path
import os
from zoneinfo import ZoneInfo

from breadth import calculate_breadth
from bar_store import ROOT as DATA_ROOT, load_bars, save_bars
from providers import alpaca_symbol, alpaca_unavailable_reason, fetch_alpaca_daily


async def download_history(symbols, endpoint, end=None, data_root=DATA_ROOT):
    """Fetch all available daily history, paging backwards without a start cutoff."""
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    token = os.environ.get("TRADINGVIEW_MCP_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else None
    series = {}
    notices = set()
    async with streamablehttp_client(endpoint, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            available = await session.list_tools()
            names = [tool.name for tool in available.tools if tool.name.endswith("get_ohlcv")]
            if len(names) != 1:
                raise ValueError("Endpoint must expose one get_ohlcv tool")
            for symbol in dict.fromkeys(symbols):
                cursor = end.isoformat() if end else None
                seen_cursors = set()
                bars = {}
                while True:
                    arguments = {"symbol": symbol, "interval": "1D", "count": 5000}
                    if cursor:
                        arguments["date_to"] = cursor
                    result = await session.call_tool(names[0], arguments)
                    if result.isError:
                        raise ValueError(f"Provider failed for {symbol}")
                    page = result.structuredContent or json.loads(next(c.text for c in result.content if c.type == "text"))
                    if not page.get("success") or not page.get("bars"):
                        raise ValueError(f"No history returned for {symbol}")
                    if page.get("notice"):
                        notices.add(page["notice"])
                    for bar in page["bars"]:
                        bars[bar["t"]] = bar
                    if not page.get("has_more"):
                        break
                    cursor = page.get("next_date_to")
                    if not cursor or cursor in seen_cursors:
                        raise ValueError(f"Invalid pagination for {symbol}")
                    seen_cursors.add(cursor)
                series[symbol] = [bars[t] for t in sorted(bars)]
                save_bars({"schema_version": 1, "provider": "tradingview",
                           "fetched_at": datetime.now(timezone.utc).isoformat(),
                           "series": {symbol: series[symbol]}, "notices": sorted(notices)}, data_root)
    return {"schema_version": 1, "provider": "tradingview", "series": series, "notices": sorted(notices),
            "fetched_at": datetime.now(timezone.utc).isoformat()}


def alpaca_source(symbols, args):
    """Read or download Alpaca bars; return (payload, prices keyed by requested symbol, unavailable)."""
    tickers = {s: alpaca_symbol(s) for s in symbols}
    unavailable = {s: alpaca_unavailable_reason(s) for s, t in tickers.items() if t is None}
    wanted = list(dict.fromkeys(t for t in tickers.values() if t))
    if not wanted:
        raise ValueError("None of the requested symbols are available from Alpaca")
    if args.alpaca:
        payload = fetch_alpaca_daily(wanted, args.history_start, args.end, feed=args.alpaca_feed,
                                     adjustment=args.adjustment)
        for ticker in payload.pop("empty_symbols"):
            unavailable.update({s: "Alpaca returned no daily bars for this ticker." for s, t in tickers.items() if t == ticker})
        saved = save_bars(payload, args.data_root)
        source = load_bars(list(payload["series"]), args.data_root, provider="alpaca", download_date=saved[0].parent.name)
    else:
        source = load_bars(wanted, args.data_root, provider="alpaca",
                           download_date=args.download_date.isoformat() if args.download_date else None)
    by_ticker = prices_from_snapshot(source)
    prices = {s: by_ticker[t] for s, t in tickers.items() if t in by_ticker}
    return source, prices, unavailable


def prices_from_snapshot(payload):
    prices = {}
    exchange_timezones = {"ASX": "Australia/Sydney", "HKEX": "Asia/Hong_Kong",
                          "IDX": "Asia/Jakarta", "LSE": "Europe/London",
                          "NYSE": "America/New_York", "NASDAQ": "America/New_York",
                          "AMEX": "America/New_York", "TSX": "America/Toronto",
                          "TSXV": "America/Toronto", "BIVA": "America/Mexico_City"}
    for symbol, bars in payload["series"].items():
        history = {}
        zone = payload.get("session_timezones", {}).get(symbol)
        if not zone and payload.get("provider") == "tradingview":
            zone = exchange_timezones.get(symbol.split(":")[0])
        session_zone = ZoneInfo(zone) if zone else timezone.utc
        for bar in bars:
            day = (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=bar["t"])).astimezone(session_zone).date().isoformat()
            if day in history:
                raise ValueError(f"Duplicate daily observation for {symbol} on {day}")
            history[day] = bar["c"]
        prices[symbol] = history
    return prices


def holdings_symbols(path):
    """Read issuer ticker labels from the GDX knowledge holdings table, excluding cash."""
    symbols = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 3 or cells[0] == "Issuer ticker" or "cash" in cells[1].lower():
            continue
        symbols.append(cells[0].replace("\\*", "*"))
    if not symbols:
        raise ValueError("No holdings found in the supplied Markdown file")
    return symbols


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    universe = parser.add_mutually_exclusive_group(required=True)
    universe.add_argument("--symbols", nargs="+", help="Symbols matching keys in the input snapshot")
    universe.add_argument("--holdings-md", type=Path, help="Use all security ticker labels from a knowledge holdings table")
    parser.add_argument("--symbol-map", type=Path, help="JSON map from issuer ticker labels to provider symbols; requires every holding")
    data = parser.add_mutually_exclusive_group()
    data.add_argument("--input", type=Path, help="Daily snapshot with series: {symbol: [{t, c}, ...]}")
    data.add_argument("--mcp-url", help="Fetch full daily history from a TradingView MCP endpoint")
    data.add_argument("--alpaca", action="store_true", help="Fetch daily history from Alpaca (US listings only; needs APCA_API_KEY_ID/APCA_API_SECRET_KEY)")
    parser.add_argument("--provider", choices=["tradingview", "alpaca"], default="tradingview",
                        help="Provider whose stored bars to read; --alpaca implies alpaca")
    parser.add_argument("--alpaca-feed", choices=["iex", "sip"], default="iex", help="Alpaca feed; iex is free but not the consolidated close")
    parser.add_argument("--adjustment", choices=["raw", "split", "dividend", "all"], default="split", help="Alpaca price adjustment")
    parser.add_argument("--history-start", type=date.fromisoformat, default=date(2016, 1, 1), help="First date requested from Alpaca")
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT, help="Raw bar root (default data/research)")
    parser.add_argument("--download-date", type=date.fromisoformat, help="Read a specific dated batch; default latest complete batch")
    parser.add_argument("--ma", type=int, default=50)
    parser.add_argument("--start", type=date.fromisoformat)
    parser.add_argument("--end", type=date.fromisoformat)
    parser.add_argument("--min-coverage", type=float, default=0.0)
    parser.add_argument("--name", default=None)
    parser.add_argument("--universe-as-of", type=date.fromisoformat)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        symbols = holdings_symbols(args.holdings_md) if args.holdings_md else args.symbols
        issuer_symbols = symbols[:]
        if args.symbol_map:
            mapping = json.loads(args.symbol_map.read_text(encoding="utf-8"))
            symbols = [mapping[s] for s in symbols]
            if len(set(symbols)) != len(symbols):
                raise ValueError("Symbol map must not map different constituents to the same provider symbol")
        unavailable = {}
        prices = None
        if args.alpaca:
            args.provider = "alpaca"
            if args.download_date:
                raise ValueError("--download-date selects stored bars; do not combine with --alpaca")
        if args.input:
            source = json.loads(args.input.read_text(encoding="utf-8"))
        elif args.provider == "alpaca":
            source, prices, unavailable = alpaca_source(symbols, args)
        elif args.mcp_url:
            if args.download_date:
                raise ValueError("--download-date selects stored bars; do not combine with --mcp-url")
            asyncio.run(download_history(symbols, args.mcp_url, args.end, args.data_root))
            source = load_bars(symbols, args.data_root)
        else:
            source = load_bars(symbols, args.data_root, provider="tradingview",
                               download_date=args.download_date.isoformat() if args.download_date else None)
        snapshot = calculate_breadth(symbols, prices if prices is not None else prices_from_snapshot(source), args.ma,
                                     start=args.start, end=args.end, min_coverage=args.min_coverage,
                                     name=args.name, universe_as_of=args.universe_as_of.isoformat() if args.universe_as_of else None)
        snapshot["input_provider"] = source.get("provider")
        snapshot["input_fetched_at"] = source.get("fetched_at")
        snapshot["input_notices"] = source.get("notices", [])
        snapshot["input_bar_files"] = source.get("bar_files", [])
        snapshot["input_sha256"] = hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest()
        snapshot["universe"]["issuer_symbols"] = issuer_symbols
        # Symbols the provider cannot supply count as missing, with the reason kept.
        snapshot["universe"]["provider_unavailable"] = unavailable
        if source.get("provider") == "alpaca":
            snapshot["input_feed"] = source.get("feed")
            snapshot["input_adjustment"] = source.get("adjustment")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(snapshot, indent=2, allow_nan=False), encoding="utf-8")
        bars = next(iter(snapshot["series"].values()))
        print(f"Saved {len(bars)} daily observations for {len(symbols)} constituents to {args.output}")
        if snapshot["universe"]["missing_symbols"]:
            print("WARNING: Missing histories: " + ", ".join(snapshot["universe"]["missing_symbols"]))
        if unavailable:
            print(f"LIMITATION: {len(unavailable)} of {len(symbols)} symbols are not available from {source.get('provider')}; breadth covers the rest only")
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.error(str(error))
    except Exception as error:
        parser.error(f"Provider operation failed ({type(error).__name__}); check endpoint and authentication")


if __name__ == "__main__":
    main()
