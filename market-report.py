"""Generate an archived market breadth report with uv run market-report.py."""

from __future__ import annotations

import argparse
import asyncio
from calendar import monthrange
from datetime import date, datetime, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
SYMBOLS = ("INDEX:MMOH", "INDEX:MMOF")
COLORS = ("#55d6be", "#ffbf69")


def months_before(day: date, months: int) -> date:
    year, month = divmod(day.year * 12 + day.month - 1 - months, 12)
    return date(year, month + 1, min(day.day, monthrange(year, month + 1)[1]))


def bar_date(bar: dict) -> date:
    return datetime.fromtimestamp(bar["t"], timezone.utc).date()


def read_snapshot(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("provider") != "tradingview" or "series" not in payload:
        raise ValueError("Expected a TradingView snapshot containing provider and series")
    return payload


async def fetch_tradingview(endpoint: str, as_of: date, start: date) -> dict:
    # Authentication stays in the environment and is never written to reports.
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    token = os.environ.get("TRADINGVIEW_MCP_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else None
    series = {}
    async with streamablehttp_client(endpoint, headers=headers, timeout=30, sse_read_timeout=60) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            available = await session.list_tools()
            candidates = [t.name for t in available.tools if t.name.endswith("get_ohlcv")]
            if len(candidates) != 1:
                raise ValueError("MCP endpoint must expose one TradingView get_ohlcv tool")
            for symbol in SYMBOLS:
                result = await session.call_tool(candidates[0], {
                    "symbol": symbol, "interval": "1D", "count": 5000,
                    "date_from": start.isoformat(), "date_to": as_of.isoformat(),
                })
                if result.isError:
                    raise ValueError(f"TradingView failed for {symbol}")
                data = result.structuredContent
                if not data:
                    data = json.loads(next(c.text for c in result.content if c.type == "text"))
                if not data.get("success") or not data.get("bars"):
                    raise ValueError(f"TradingView returned no bars for {symbol}")
                if data.get("has_more"):
                    raise ValueError("Requested history exceeds one response; shorten --lookback")
                series[symbol] = data["bars"]
    return {"schema_version": 1, "provider": "tradingview",
            "fetched_at": datetime.now(timezone.utc).isoformat(), "series": series}


def build_report(payload: dict, requested: date, lookback: int, source: str,
                 today: date | None = None) -> dict:
    today = today or datetime.now(ZoneInfo("America/New_York")).date()
    # Today's daily bar may still be forming. This PoC only uses previous dates.
    cutoff = min(requested, today - timedelta(days=1))
    start = months_before(requested, lookback)
    series = {}
    warnings = []
    for symbol in SYMBOLS:
        unique = {}
        for bar in payload["series"].get(symbol, []):
            observed = bar_date(bar)
            if observed <= cutoff and bar.get("c") is not None:
                unique[observed] = {"date": observed.isoformat(), "close": float(bar["c"])}
        history = [unique[d] for d in sorted(unique)]
        visible = [b for b in history if date.fromisoformat(b["date"]) >= start]
        if not visible:
            raise ValueError(f"No observations for {symbol} in requested date window")
        latest = history[-1]
        previous = history[-2] if len(history) > 1 else None
        fifth = history[-6] if len(history) > 5 else None
        lag = (requested - date.fromisoformat(latest["date"])).days
        if lag > 3:
            warnings.append(f"{symbol}: latest observation is {lag} calendar days before requested date.")
        if date.fromisoformat(visible[0]["date"]) > start + timedelta(days=7):
            warnings.append(f"{symbol}: available history starts {visible[0]['date']}; lookback is incomplete.")
        series[symbol] = {"latest": latest, "daily_change": round(latest["close"] - previous["close"], 4) if previous else None,
                          "five_session_change": round(latest["close"] - fifth["close"], 4) if fifth else None,
                          "observations": visible}
    dates = {s["latest"]["date"] for s in series.values()}
    if len(dates) > 1:
        warnings.append("Indicators have different latest observation dates.")
    return {"schema_version": 1, "title": "Daily situational awareness · Market breadth",
            "requested_date": requested.isoformat(), "observation_cutoff": cutoff.isoformat(),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "provider": payload["provider"], "data_fetched_at": payload.get("fetched_at"),
            "source": source, "lookback_months": lookback, "warnings": warnings,
            "daily_bar_policy": "Exclude the current New York calendar date; no exchange-calendar inference.",
            "historical_note": "Historical mode filters observations by date; provider revisions are not reconstructed.",
            "series": series}


def change_text(value: float | None) -> str:
    return "unavailable" if value is None else f"{value:+.2f} points"


def chart_svg(report: dict) -> str:
    observations = [b for s in report["series"].values() for b in s["observations"]]
    first = min(date.fromisoformat(b["date"]).toordinal() for b in observations)
    last = max(date.fromisoformat(b["date"]).toordinal() for b in observations)
    low = min(b["close"] for b in observations)
    high = max(b["close"] for b in observations)
    padding = max((high - low) * .1, 1)
    low, high = low - padding, high + padding
    x = lambda day: 65 + (date.fromisoformat(day).toordinal() - first) / max(last - first, 1) * 890
    y = lambda val: 300 - (val - low) / (high - low) * 265
    parts = ['<svg viewBox="0 0 1000 350" role="img" aria-label="MMOH and MMOF daily closing values over time">']
    for i in range(5):
        value = low + (high - low) * i / 4
        position = y(value)
        parts.append(f'<line x1="65" x2="955" y1="{position}" y2="{position}" stroke="#2d3c50"/><text x="52" y="{position+4}" text-anchor="end">{value:.1f}</text>')
    for symbol, color in zip(SYMBOLS, COLORS):
        bars = report["series"][symbol]["observations"]
        points = " ".join(f'{x(b["date"]):.2f},{y(b["close"]):.2f}' for b in bars)
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        b = bars[-1]
        parts.append(f'<circle cx="{x(b["date"])}" cy="{y(b["close"])}" r="4" fill="{color}"><title>{symbol}: {b["close"]:.2f} on {b["date"]}</title></circle>')
    for ordinal, anchor in ((first, "start"), (last, "end")):
        pos = 65 if anchor == "start" else 955
        parts.append(f'<text x="{pos}" y="330" text-anchor="{anchor}">{date.fromordinal(ordinal).isoformat()}</text>')
    return "".join(parts) + "</svg>"


def breadth_interpretation(report: dict) -> str:
    series = [report["series"][symbol] for symbol in SYMBOLS]
    daily = [s["daily_change"] for s in series]
    weekly = [s["five_session_change"] for s in series]
    if all(v is not None and v < 0 for v in daily):
        recap = "Both breadth indicators weakened in their latest sessions."
    elif all(v is not None and v > 0 for v in daily):
        recap = "Both breadth indicators strengthened in their latest sessions."
    else:
        recap = "The latest readings show mixed, unchanged, or incomplete breadth signals."
    if all(v is not None and v > 0 for v in weekly):
        recap += " Both remain above their levels five sessions earlier, indicating an improving short-term trend."
    elif all(v is not None and v < 0 for v in weekly):
        recap += " Both are below their levels five sessions earlier, indicating a weakening short-term trend."
    return recap


def render_section(title: str, visual: str, interpretation: str) -> str:
    """Shared report template: one chart or table followed by a brief interpretation."""
    return f'<section class="section"><h2>{escape(title)}</h2>{visual}<p class="interpretation">{escape(interpretation)}</p></section>'


def render_html(report: dict) -> str:
    legend = "".join(
        f'<span style="color:{color}">{symbol.split(":")[1]} {report["series"][symbol]["latest"]["close"]:.2f}</span>'
        for symbol, color in zip(SYMBOLS, COLORS)
    )
    dates = sorted({s["latest"]["date"] for s in report["series"].values()})
    visual = f'<div class="legend">{legend}</div>{chart_svg(report)}<small>Observed {escape(" / ".join(dates))} · TradingView · {report["lookback_months"]}-month view</small>'
    section = render_section("Market breadth", visual, breadth_interpretation(report))
    warnings = "".join(f'<p class="warning">{escape(w)}</p>' for w in report["warnings"])
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Market report · {report['requested_date']}</title>
<style>body{{background:#0b1220;color:#e4edf8;font:16px system-ui;margin:0}}main{{max-width:1000px;margin:auto;padding:32px 24px}}h1{{font-size:24px;font-weight:500;margin-bottom:32px}}h1 small{{font-size:14px;color:#aebed1}}h2{{font-size:20px;margin:0 0 20px}}.section{{margin-bottom:40px}}svg{{width:100%;height:auto}}svg text{{fill:#aebed1;font-size:12px}}.legend{{display:flex;gap:24px;font-size:14px}}small{{color:#aebed1;font-size:12px}}.interpretation{{line-height:1.65;max-width:85ch}}.warning{{background:#4c3617;padding:12px;border-radius:8px}}</style>
<main><h1>Daily situational awareness <small>{report['requested_date']}</small></h1>{warnings}{section}</main></html>'''


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["daily"], nargs="?", default="daily")
    parser.add_argument("--date", type=date.fromisoformat, default=None, help="As-of date YYYY-MM-DD; default today in New York")
    parser.add_argument("--provider", choices=["snapshot", "tradingview"], default="snapshot")
    parser.add_argument("--snapshot", type=Path, default=ROOT / "data/tradingview-breadth.json")
    parser.add_argument("--mcp-url", default=os.environ.get("TRADINGVIEW_MCP_URL", "https://mcp.tradingview.com/mcp"), help="Streamable HTTP MCP endpoint; or TRADINGVIEW_MCP_URL")
    parser.add_argument("--lookback", type=int, default=6, metavar="MONTHS")
    parser.add_argument("--format", default="html,json", help="html, json, or html,json")
    parser.add_argument("--output", type=Path, default=ROOT / "reports")
    parser.add_argument("--refresh", action="store_true", help="Refresh live-provider cache")
    args = parser.parse_args(argv)
    formats = set(args.format.split(","))
    if not formats or not formats <= {"html", "json"}:
        parser.error("--format must be html, json, or html,json")
    if not 1 <= args.lookback <= 120:
        parser.error("--lookback must be between 1 and 120 months")
    today = datetime.now(ZoneInfo("America/New_York")).date()
    requested = args.date or today
    if requested > today:
        parser.error("--date cannot be in the future")
    try:
        if args.provider == "snapshot":
            if args.refresh:
                parser.error("--refresh requires --provider tradingview")
            payload = read_snapshot(args.snapshot)
            source = f"snapshot: {args.snapshot.name}"
        else:
            if not args.mcp_url:
                parser.error("--provider tradingview requires --mcp-url or TRADINGVIEW_MCP_URL")
            cache = ROOT / ".cache" / f"tradingview-{requested}-{args.lookback}m.json"
            if cache.exists() and not args.refresh:
                payload = read_snapshot(cache)
                source = "TradingView MCP (cached)"
            else:
                payload = asyncio.run(fetch_tradingview(args.mcp_url, min(requested, today - timedelta(days=1)), months_before(requested, args.lookback) - timedelta(days=20)))
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps(payload, indent=2), encoding="utf-8")
                source = "TradingView MCP (fresh)"
        report = build_report(payload, requested, args.lookback, source, today)
        args.output.mkdir(parents=True, exist_ok=True)
        for fmt in sorted(formats):
            path = args.output / f"market-report-{requested}.{fmt}"
            content = render_html(report) if fmt == "html" else json.dumps(report, indent=2, allow_nan=False)
            path.write_text(content, encoding="utf-8")
            print(f"Saved {path.resolve()}")
        for symbol, s in report["series"].items():
            print(f'{symbol}: {s["latest"]["close"]:.2f} | daily {change_text(s["daily_change"])} | observed {s["latest"]["date"]}')
        for warning in report["warnings"]:
            print(f"WARNING: {warning}", file=sys.stderr)
        return 0
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        # MCP transport errors can contain request headers; avoid logging them.
        print(f"Error: provider operation failed ({type(exc).__name__}). Check endpoint and authentication.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
