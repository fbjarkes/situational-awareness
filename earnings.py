"""Download and cache TradingView quarterly revenue and EPS as readable JSON.

Run: uv run earnings.py NASDAQ:MSFT --years 5
"""
from __future__ import annotations

import argparse
import asyncio
from calendar import monthrange
from datetime import date, datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent / "data/earnings"
ENDPOINT = "https://mcp.tradingview.com/mcp"


def cache_path(symbol: str, data_root: Path = ROOT) -> Path:
    if not isinstance(symbol, str) or ":" not in symbol or any(not p.strip() for p in symbol.split(":", 1)):
        raise ValueError("Use a canonical EXCHANGE:TICKER symbol, e.g. NASDAQ:MSFT")
    return Path(data_root) / (quote(symbol, safe="") + ".json")


def request_window(years: int, end: date | str | None = None) -> tuple[date, date]:
    if isinstance(years, bool) or not isinstance(years, int) or years < 1:
        raise ValueError("years must be a positive integer")
    end = date.fromisoformat(end) if isinstance(end, str) else end
    end = end or datetime.now(ZoneInfo("Europe/Stockholm")).date()
    year = end.year - years
    start = date(year, end.month, min(end.day, monthrange(year, end.month)[1]))
    return start, end


def save_earnings_response(symbol: str, response: dict, *, start: date, end: date,
                           fetched_at: str, data_root: Path = ROOT) -> dict:
    """Archive a connector or HTTP response without changing provider labels.

    Connected-tool callers supply the actual response receipt timestamp.
    Structural errors fail before replacing any existing cache.
    """
    path = cache_path(symbol, data_root)
    instant = datetime.fromisoformat(fetched_at.replace("Z", "+00:00"))
    if instant.tzinfo is None:
        raise ValueError("fetched_at must include a timezone")
    if response.get("success") is not True or response.get("symbol") != symbol or response.get("period") != "fq":
        raise ValueError("Expected a successful quarterly response for the requested symbol")
    labels, series = response.get("labels"), response.get("series")
    if not isinstance(labels, list) or not labels or not all(isinstance(label, str) and label for label in labels):
        raise ValueError("TradingView returned no valid quarterly labels")
    if not isinstance(series, dict):
        raise ValueError("TradingView returned no financial series")
    warnings, rows = [], []
    for metric in ("revenue", "eps"):
        if not isinstance(series.get(metric), list) or len(series[metric]) != len(labels):
            raise ValueError(f"{metric} values do not align with quarter labels")
    for i, label in enumerate(labels):
        row = {"provider_index": i, "period_label": label}
        for metric in ("revenue", "eps"):
            point = series[metric][i]
            if not isinstance(point, dict):
                raise ValueError(f"Invalid {metric} observation")
            for field, suffix in (("value", ""), ("yoy_pct", "_yoy_pct")):
                value = point.get(field)
                if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)):
                    raise ValueError(f"Invalid {metric} {field}")
                row[metric + suffix] = value
        rows.append(row)
    duplicates = sorted({label for label in labels if labels.count(label) > 1})
    if duplicates:
        warnings.append("Duplicate provider quarter labels: " + ", ".join(duplicates) + ". Do not infer corrected quarter dates.")
    if any(row[metric] is None for row in rows for metric in ("revenue", "eps")):
        warnings.append("Some revenue/EPS observations are unavailable (null), not zero.")
    warnings.append("Requested date window does not guarantee complete history; no missing quarters are fabricated.")
    currency = response.get("currency")
    eps_basis = response.get("eps_basis")
    if currency is None:
        warnings.append("Reporting currency and scale are not specified by this response; values are preserved as supplied.")
    if eps_basis is None:
        warnings.append("EPS basis (basic/diluted, GAAP/adjusted) is not specified by this response.")
    canonical = json.dumps(response, sort_keys=True, separators=(",", ":"), allow_nan=False)
    payload = {"schema_version": 1, "provider": "tradingview", "symbol": symbol,
               "period": "fq", "fetched_at": fetched_at,
               "download_date": instant.astimezone(ZoneInfo("Europe/Stockholm")).date().isoformat(),
               "request": {"date_from": start.isoformat(), "date_to": end.isoformat(), "period": "fq"},
               "currency": currency, "eps_basis": eps_basis, "observation_count": len(rows),
               "unique_period_labels": len(set(labels)), "warnings": warnings,
               "quarters": rows, "provider_response_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
               "provider_response": response}
    path.parent.mkdir(parents=True, exist_ok=True)
    # Unique temporary file plus atomic replace avoids partial readable caches.
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, suffix=".tmp", delete=False) as handle:
            temp_path = Path(handle.name)
            json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.write("\n")
        temp_path.replace(path)
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()
    return payload


async def fetch_financial_history(symbol: str, start: date, end: date, *, endpoint: str) -> dict:
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    token = os.environ.get("TRADINGVIEW_MCP_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else None
    async with streamablehttp_client(endpoint, headers=headers, timeout=30, sse_read_timeout=60) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            catalog = await session.list_tools()
            names = [tool.name for tool in catalog.tools if tool.name.endswith("get_financial_history")]
            if len(names) != 1:
                raise ValueError("MCP endpoint must expose one get_financial_history tool")
            result = await session.call_tool(names[0], {"symbol": symbol, "period": "fq",
                                                       "date_from": start.isoformat(), "date_to": end.isoformat()})
            if result.isError:
                raise ValueError(f"TradingView financial-history request failed for {symbol}")
            return result.structuredContent or json.loads(next(c.text for c in result.content if c.type == "text"))


def download_earnings(symbol: str, years: int = 5, *, end: date | str | None = None,
                      refresh: bool = False,
                      data_root: Path = ROOT, endpoint: str | None = None, fetcher=None) -> dict:
    """Return quarterly revenue/EPS, always reusing a matching cached window.

    `fetcher(symbol, start, end)` optionally injects a synchronous provider client.
    Returns saved metadata and readable `quarters` rows; never merges windows.
    Failures propagate and preserve any prior cache; stale data is not substituted.
    """
    path = cache_path(symbol, data_root)
    start, end = request_window(years, end)
    expected = {"date_from": start.isoformat(), "date_to": end.isoformat(), "period": "fq"}
    if path.exists() and not refresh:
        try:
            cached = json.loads(path.read_text(encoding="utf-8"))
            if (cached.get("schema_version") == 1 and cached.get("provider") == "tradingview"
                    and cached.get("symbol") == symbol and cached.get("request") == expected
                    and isinstance(cached.get("quarters"), list) and cached["quarters"]):
                return cached
        except (ValueError, KeyError, TypeError):
            pass  # Malformed cache is replaced only after a successful fetch.
    response = (fetcher(symbol, start, end) if fetcher else
                asyncio.run(fetch_financial_history(symbol, start, end,
                            endpoint=endpoint or os.environ.get("TRADINGVIEW_MCP_URL", ENDPOINT))))
    return save_earnings_response(symbol, response, start=start, end=end,
                                  fetched_at=datetime.now(timezone.utc).isoformat(), data_root=data_root)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbol", help="Canonical TradingView symbol, e.g. NASDAQ:MSFT")
    parser.add_argument("--years", type=int, default=5)
    parser.add_argument("--end", type=date.fromisoformat, help="Window end; defaults to today in Stockholm")
    parser.add_argument("--refresh", action="store_true", help="Ignore cache freshness and download again")
    parser.add_argument("--data-root", type=Path, default=ROOT)
    parser.add_argument("--mcp-url", help="Or set TRADINGVIEW_MCP_URL; auth via TRADINGVIEW_MCP_TOKEN")
    args = parser.parse_args(argv)
    try:
        payload = download_earnings(args.symbol, args.years, end=args.end, refresh=args.refresh,
                                    data_root=args.data_root, endpoint=args.mcp_url)
    except Exception:
        # Transport exceptions may contain auth headers; don't print them.
        print("Earnings download failed. Check symbol, arguments, TradingView MCP access and authentication; prior cache was preserved.", file=sys.stderr)
        return 1
    print(f'{cache_path(args.symbol, args.data_root)}: {payload["observation_count"]} observations; fetched {payload["fetched_at"]}')
    for warning in payload["warnings"]:
        print(f"NOTE: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
