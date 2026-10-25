"""Calculate custom breadth from a daily snapshot; all downloads stay in data/."""
import argparse
import asyncio
from datetime import date, datetime, timedelta, timezone
import json
import hashlib
from pathlib import Path
import os
from zoneinfo import ZoneInfo

from breadth import calculate_breadth


async def download_history(symbols, endpoint, end=None):
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
    return {"schema_version": 1, "provider": "tradingview", "series": series, "notices": sorted(notices),
            "fetched_at": datetime.now(timezone.utc).isoformat()}


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
    data = parser.add_mutually_exclusive_group(required=True)
    data.add_argument("--input", type=Path, help="Daily snapshot with series: {symbol: [{t, c}, ...]}")
    data.add_argument("--mcp-url", help="Fetch full daily history from a TradingView MCP endpoint")
    parser.add_argument("--save-prices", type=Path, help="Save downloaded raw snapshot, normally under data/")
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
        source = json.loads(args.input.read_text(encoding="utf-8")) if args.input else asyncio.run(download_history(symbols, args.mcp_url, args.end))
        if args.save_prices:
            args.save_prices.parent.mkdir(parents=True, exist_ok=True)
            args.save_prices.write_text(json.dumps(source, allow_nan=False), encoding="utf-8")
        snapshot = calculate_breadth(symbols, prices_from_snapshot(source), args.ma,
                                     start=args.start, end=args.end, min_coverage=args.min_coverage,
                                     name=args.name, universe_as_of=args.universe_as_of.isoformat() if args.universe_as_of else None)
        snapshot["input_provider"] = source.get("provider")
        snapshot["input_fetched_at"] = source.get("fetched_at")
        snapshot["input_notices"] = source.get("notices", [])
        snapshot["input_sha256"] = hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest()
        snapshot["universe"]["issuer_symbols"] = issuer_symbols
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(snapshot, indent=2, allow_nan=False), encoding="utf-8")
        bars = next(iter(snapshot["series"].values()))
        print(f"Saved {len(bars)} daily observations for {len(symbols)} constituents to {args.output}")
        if snapshot["universe"]["missing_symbols"]:
            print("WARNING: Missing histories: " + ", ".join(snapshot["universe"]["missing_symbols"]))
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.error(str(error))
    except Exception as error:
        parser.error(f"Provider operation failed ({type(error).__name__}); check endpoint and authentication")


if __name__ == "__main__":
    main()
