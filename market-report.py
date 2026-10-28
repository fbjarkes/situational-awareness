"""Generate an archived market breadth report with uv run market-report.py."""

from __future__ import annotations

import argparse
import asyncio
from calendar import monthrange
from datetime import date, datetime, time, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
import sys
import hashlib
import yaml
from zoneinfo import ZoneInfo
from bar_store import ROOT as DATA_ROOT, load_bars, save_bars
from research_todos import collect_research_todos
from providers import alpaca_symbol, alpaca_unavailable_reason, fetch_alpaca_daily, provider_label
from price_stats import (cons_days_above_ma, cons_days_below_ma, cons_down_days, distance_from_ma,
                         streak_is_lower_bound, lowest_close_period)

ROOT = Path(__file__).resolve().parent
SYMBOLS = ("INDEX:MMOH", "INDEX:MMOF")
COLORS = ("#67ddc4", "#ffc078")
NY = ZoneInfo("America/New_York")
MARKET_CLOSE = time(16, 0)
SPY_SYMBOLS = {"tradingview": "AMEX:SPY", "alpaca": "SPY"}
# Calendar days of SPY history: enough for a 200-day SMA plus long streaks.
SPY_HISTORY_DAYS = 1100
VIX_SYMBOL = "CBOE:VIX"


def months_before(day: date, months: int) -> date:
    year, month = divmod(day.year * 12 + day.month - 1 - months, 12)
    return date(year, month + 1, min(day.day, monthrange(year, month + 1)[1]))


def bar_date(bar: dict) -> date:
    return (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=bar["t"])).date()


def read_snapshot(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not payload.get("provider") or "series" not in payload:
        raise ValueError("Expected a snapshot containing provider and series")
    return payload


async def fetch_tradingview(endpoint: str, as_of: date, start: date, symbols: tuple[str, ...] = SYMBOLS) -> dict:
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
            for symbol in symbols:
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


def observation_cutoff(requested: date, today: date, close_only: bool) -> date:
    return min(requested, today - timedelta(days=1)) if close_only else requested


def build_report(payload: dict, requested: date, lookback: int, source: str,
                 now: datetime | None = None, close_only: bool = False,
                 symbols: tuple[str, ...] = SYMBOLS) -> dict:
    now = (now or datetime.now(NY)).astimezone(NY)
    today = now.date()
    cutoff = observation_cutoff(requested, today, close_only)
    # A bar dated on the fetch day, fetched before 16:00 ET, is still forming.
    fetched = payload.get("fetched_at")
    start = months_before(requested, lookback)
    series = {}
    warnings = []
    for symbol in symbols:
        symbol_fetched = payload.get("symbol_fetched_at", {}).get(symbol, fetched)
        symbol_fetched_ny = datetime.fromisoformat(symbol_fetched.replace("Z", "+00:00")).astimezone(NY) if symbol_fetched else now
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
        intraday = date.fromisoformat(latest["date"]) == symbol_fetched_ny.date() and symbol_fetched_ny.time() < MARKET_CLOSE
        as_of = (f"intraday {latest['date']} {symbol_fetched_ny:%H:%M} ET" if intraday else f"close {latest['date']}")
        series[symbol] = {"latest": latest, "latest_status": "intraday" if intraday else "close", "as_of": as_of, "fetched_at": symbol_fetched,
                          "daily_change": round(latest["close"] - previous["close"], 4) if previous else None,
                          "five_session_change": round(latest["close"] - fifth["close"], 4) if fifth else None,
                          "observations": visible}
    mixed = len({s["as_of"] for s in series.values()}) > 1
    notes = ["Readings come from different dates or times; each line below says which."] if mixed else []
    for symbol, s in series.items():
        name = symbol.split(":")[-1]
        if s["latest_status"] == "intraday":
            notes.append(f"{name}: {s['as_of']}; not a closing value. "
                         "Changes compare it with the previous close.")
        elif mixed or (requested == today and s["latest"]["date"] < requested.isoformat()):
            notes.append(f"{name}: using the {s['latest']['date']} close; no newer reading was available.")
    return {"schema_version": 1, "title": "Daily situational awareness · Market breadth",
            "requested_date": requested.isoformat(), "observation_cutoff": cutoff.isoformat(),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "provider": payload["provider"], "data_fetched_at": payload.get("fetched_at"),
            "input_bar_files": payload.get("bar_files", []),
            "source": source, "lookback_months": lookback, "warnings": warnings, "notes": notes,
            "daily_bar_policy": ("Exclude the current New York calendar date." if close_only else
                                 "Include today's bar when available; label it intraday if fetched before 16:00 ET."),
            "historical_note": "Historical mode filters observations by date; provider revisions are not reconstructed.",
            "series": series}


def breadth_metadata(symbol: str) -> dict:
    filename = symbol.split(":")[-1].lower() + ".md"
    for folder in ("breadth", "index"):
        path = ROOT / "knowledge" / folder / filename
        if path.exists():
            return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
    return {}


def provider_availability(symbol: str, provider: str) -> dict:
    """Availability of a report series from a provider, as recorded in the knowledge bundle."""
    recorded = breadth_metadata(symbol).get("market_report", {}).get("data_providers", {}).get(provider)
    if recorded:
        return recorded
    if provider == "alpaca" and alpaca_symbol(symbol) is None:
        return {"status": "unavailable", "reason": alpaca_unavailable_reason(symbol)}
    return {"status": "available", "symbol": symbol}


def unavailable_report(requested: date, lookback: int, close_only: bool, reason: str) -> dict:
    """A report shell whose breadth section explains why it has no data."""
    return {"schema_version": 1, "title": "Daily situational awareness · Market breadth",
            "requested_date": requested.isoformat(), "observation_cutoff": requested.isoformat(),
            "generated_at": datetime.now(timezone.utc).isoformat(), "provider": None,
            "data_fetched_at": None, "input_bar_files": [], "source": "unavailable",
            "lookback_months": lookback, "warnings": [], "notes": [],
            "daily_bar_policy": ("Exclude the current New York calendar date." if close_only else
                                 "Include today's bar when available; label it intraday if fetched before 16:00 ET."),
            "historical_note": "Historical mode filters observations by date; provider revisions are not reconstructed.",
            "series": {}, "breadth_unavailable": reason}


def spy_section(payload: dict | None, provider: str, requested: date, lookback: int, now: datetime,
                close_only: bool, source: str, unavailable: str | None = None) -> dict:
    """Latest SPY trend metrics; descriptive only, no thresholds are applied."""
    symbol = SPY_SYMBOLS[provider]
    if payload is None or not payload["series"].get(symbol):
        return {"symbol": symbol, "provider": provider, "unavailable": unavailable or f"No stored {symbol} history was found."}
    base = build_report(payload, requested, lookback, source, now, close_only, (symbol,))
    series = base["series"][symbol]
    cutoff = date.fromisoformat(base["observation_cutoff"])
    unique = {bar_date(b): float(b["c"]) for b in payload["series"][symbol] if b.get("c") is not None and bar_date(b) <= cutoff}
    closes = [unique[d] for d in sorted(unique)]
    above, below, down = cons_days_above_ma(closes, 50), cons_days_below_ma(closes, 50), cons_down_days(closes)
    metrics = {"close": closes[-1],
               "distance_from_sma200_pct": distance_from_ma(closes, 200),
               "distance_from_sma50_pct": distance_from_ma(closes, 50),
               "cons_days_above_sma50": above, "cons_days_below_sma50": below,
               "cons_down_days": down,
               "lower_bound": {"cons_days_above_sma50": streak_is_lower_bound(closes, above, 50),
                               "cons_days_below_sma50": streak_is_lower_bound(closes, below, 50),
                               "cons_down_days": streak_is_lower_bound(closes, down)},
               "history_sessions": len(closes), "history_start": min(unique).isoformat()}
    warnings = list(base["warnings"])
    if metrics["distance_from_sma200_pct"] is None:
        warnings.append(f"{symbol}: fewer than 200 sessions of history; 200-day distance unavailable.")
    return {"symbol": symbol, "provider": provider, "source": source, "as_of": series["as_of"],
            "latest_status": series["latest_status"], "latest": series["latest"],
            "fetched_at": series["fetched_at"], "daily_change": series["daily_change"],
            "input_bar_files": payload.get("bar_files", []), "feed": payload.get("feed"),
            "adjustment": payload.get("adjustment"), "metrics": metrics, "warnings": warnings,
            "definitions": {"sma": "simple average of the latest N closes, including the current close",
                            "distance": "100 * (close / SMA - 1)",
                            "streaks": "consecutive sessions ending at the latest close; ties end a streak",
                            "lower_bound": "streak reaches the start of the downloaded history"},
            "knowledge_sources": ["/index/spy.md"]}


def spy_interpretation(spy: dict) -> str:
    m = spy["metrics"]
    plural = lambda n: f'{n} session{"" if n == 1 else "s"}'
    side = (f'{plural(m["cons_days_above_sma50"])} above' if m["cons_days_above_sma50"]
            else f'{plural(m["cons_days_below_sma50"])} below')
    d200 = m["distance_from_sma200_pct"]
    where = "unavailable relative to its 200-day average" if d200 is None else f'{abs(d200):.1f}% {"above" if d200 >= 0 else "below"} its 200-day average'
    text = (f'SPY closed {where}, {side} its 50-day average, with {m["cons_down_days"]} consecutive down session{"" if m["cons_down_days"] == 1 else "s"}. '
            'These are descriptive readings; the related studies are open Research TODOs, so no threshold is interpreted.')
    if spy["latest_status"] == "intraday":
        text += " Today's value is intraday and can change before the close."
    return text


def vix_section(payload, requested, lookback, now, close_only=False, period=365):
    if payload is None or not payload.get("series", {}).get(VIX_SYMBOL):
        return {"symbol": VIX_SYMBOL, "provider": "tradingview", "unavailable": "No stored TradingView VIX history was found."}
    base = build_report(payload, requested, lookback, "TradingView bar store", now, close_only, (VIX_SYMBOL,))
    series = base["series"][VIX_SYMBOL]
    cutoff = date.fromisoformat(base["observation_cutoff"])
    history = {bar_date(b): float(b["c"]) for b in payload["series"][VIX_SYMBOL]
               if b.get("c") is not None and bar_date(b) <= cutoff}
    closes = [history[d] for d in sorted(history)]
    low = lowest_close_period(closes, period)
    limit = min(period, len(closes))
    fetched = datetime.fromisoformat(series["fetched_at"].replace("Z", "+00:00")).astimezone(NY)
    intraday = series["latest"]["date"] == fetched.date().isoformat() and fetched.time() < time(16, 15)
    as_of = f'intraday {series["latest"]["date"]} {fetched:%H:%M} ET' if intraday else f'close {series["latest"]["date"]}'
    description = (f'VIX is at a strict closing low across the latest {low} observations' if low else
                   'VIX has not made a fresh lower close relative to the preceding observation')
    text = f'{description}, describing the recent level of S&P 500 option-implied volatility rather than market direction.'
    text += (' The reading and day-low metric are provisional until the session closes.' if intraday else
             ' The day-low measure is descriptive and does not establish a trading signal.')
    return {"symbol": VIX_SYMBOL, "provider": "tradingview", "latest": series["latest"],
            "as_of": as_of, "latest_status": "intraday" if intraday else "close",
            "fetched_at": series["fetched_at"], "metrics": {"close": closes[-1], "day_low": low},
            "period": period, "history_sessions": len(closes), "history_start": min(history).isoformat(),
            "effective_lookback": limit, "day_low_lower_bound": low > 0 and low == limit,
            "interpretation": text, "warnings": base["warnings"],
            "knowledge_sources": ["/index/vix.md"], "input_bar_files": payload.get("bar_files", [])}


def change_text(value: float | None) -> str:
    return "unavailable" if value is None else f"{value:+.2f} points"


def chart_svg(report: dict, compact: bool = False) -> str:
    observations = [b for s in report["series"].values() for b in s["observations"]]
    first = min(date.fromisoformat(b["date"]).toordinal() for b in observations)
    last = max(date.fromisoformat(b["date"]).toordinal() for b in observations)
    low, high = 0, 100
    left, right = (60, 500) if compact else (65, 955)
    width = 520 if compact else 1000
    x = lambda day: left + (date.fromisoformat(day).toordinal() - first) / max(last - first, 1) * (right - left)
    y = lambda val: 300 - (val - low) / (high - low) * 265
    parts = [f'<svg viewBox="0 0 {width} 350" role="img" aria-label="Daily breadth percentages over time">']
    for i in range(5):
        value = low + (high - low) * i / 4
        position = y(value)
        parts.append(f'<line x1="{left}" x2="{right}" y1="{position}" y2="{position}" stroke="#2d3c50"/><text x="{left-12}" y="{position+4}" text-anchor="end">{value:.0f}%</text>')
    for index, (symbol, color) in enumerate(zip(report["series"], COLORS)):
        bars = report["series"][symbol]["observations"]
        points = " ".join(f'{x(b["date"]):.2f},{y(b["close"]):.2f}' for b in bars)
        dash = ' stroke-dasharray="7 4"' if index else ''
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.5"{dash}/>')
        b = bars[-1]
        parts.append(f'<circle cx="{x(b["date"])}" cy="{y(b["close"])}" r="4" fill="{color}"><title>{symbol}: {b["close"]:.2f} on {b["date"]}</title></circle>')
    ticks = [(first, "start"), (last, "end")]
    month = date.fromordinal(first).replace(day=1)
    while month.toordinal() <= last:
        if ((not compact and first + 14 < month.toordinal() < last - 14) or
                (compact and month.month % 2 == 0 and first + 35 < month.toordinal() < last - 35)):
            ticks.append((month.toordinal(), "middle"))
        month = date(month.year + (month.month == 12), month.month % 12 + 1, 1)
    for ordinal, anchor in sorted(ticks):
        day = date.fromordinal(ordinal)
        pos = x(day.isoformat())
        label = day.strftime("%d %b") if ordinal in (first, last) else day.strftime("%b '%y") if day.month == 1 else day.strftime("%b")
        parts.append(f'<text x="{pos}" y="330" text-anchor="{anchor}">{label}</text>')
    return "".join(parts) + "</svg>"


def breadth_interpretation(report: dict) -> str:
    knowledge = report.get("breadth_knowledge")
    if knowledge:
        readings = []
        crossings = []
        for symbol in SYMBOLS:
            s = report["series"][symbol]
            config = knowledge[symbol]["metadata"]["market_report"]
            readings.append(f'{symbol.split(":")[1]} at {s["latest"]["close"]:.2f}% shows the share of stocks above their {config["average_horizon_days"]}-day average')
            if s["daily_change"] is not None:
                previous = s["latest"]["close"] - s["daily_change"]
                for threshold in config["studied_crossing_thresholds"]:
                    if previous >= threshold > s["latest"]["close"]:
                        crossings.append(f'{symbol.split(":")[1]} below {threshold}')
        level = "both below half, indicating limited participation" if all(report["series"][s]["latest"]["close"] < 50 for s in SYMBOLS) else "participation differs across the two horizons"
        first = "; ".join(readings) + f" — {level}."
        if crossings:
            second = " New downward crossings: " + ", ".join(crossings) + "; the linked historical study is exploratory and does not establish a buying signal."
        else:
            second = " Neither index made a new downward crossing of 30, 25, or 20, so the study's crossing-conditioned SPY returns do not describe a fresh signal today."
        return first + second
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
    if any(s["latest_status"] == "intraday" for s in series):
        recap += " Today's values are intraday and can change before the close."
    return recap


def attach_breadth_knowledge(report: dict) -> None:
    if not report["series"]:
        return
    knowledge = {}
    for symbol in SYMBOLS:
        path = ROOT / "knowledge" / "breadth" / (symbol.split(":")[1].lower() + ".md")
        content = path.read_text(encoding="utf-8")
        metadata = yaml.safe_load(content.split("---", 2)[1])
        knowledge[symbol] = {"path": path.relative_to(ROOT).as_posix(),
                             "sha256": hashlib.sha256(content.encode()).hexdigest(),
                             "metadata": metadata, "content": content}
    report["breadth_knowledge"] = knowledge
    report["interpretation"] = breadth_interpretation(report)


def render_section(title: str, visual: str, interpretation: str) -> str:
    """Shared report template: one chart or table followed by a brief interpretation."""
    return f'<section class="section"><h2>{escape(title)}</h2>{visual}<p class="interpretation">{escape(interpretation)}</p></section>'


def attach_gdx_breadth(report: dict, path: Path, now: datetime, close_only: bool) -> None:
    if not path.exists():
        report["notes"].append("GDX breadth snapshot is unavailable; generate data/gdx-breadth-sma50.json first.")
        return
    payload = read_snapshot(path)
    symbols = tuple(payload["series"])
    if len(symbols) != 1 or payload.get("definition", {}).get("average") != "SMA":
        raise ValueError("GDX breadth snapshot must contain one custom SMA series")
    section = build_report(payload, date.fromisoformat(report["requested_date"]),
                           report["lookback_months"], path.name, now, close_only, symbols)
    series = section["series"][symbols[0]]
    latest = next(b for b in payload["series"][symbols[0]] if bar_date(b).isoformat() == series["latest"]["date"])
    section["coverage"] = {k: latest[k] for k in ("above", "below", "equal", "eligible", "universe_size", "coverage")}
    section["definition"] = payload["definition"]
    section["input_provider"] = payload.get("input_provider")
    section["provider_unavailable"] = payload["universe"].get("provider_unavailable", {})
    if section["provider_unavailable"]:
        n, size = len(section["provider_unavailable"]), len(payload["universe"]["symbols"])
        report.setdefault("provider_coverage", []).append({
            "symbol": "CUSTOM:GDX-SMA50", "label": f"{n} of {size} GDX constituents", "section": "Gold miners",
            "requested_provider": section["input_provider"], "provider_used": section["input_provider"], "status": "partial",
            "source": "breadth uses the remaining listings, so it is not comparable with full-universe history",
            "reason": "Foreign listings are not carried by this provider."})
    section["universe"] = payload["universe"]
    delta = series["five_session_change"]
    direction = (f"up {delta:.2f} percentage points over five observations" if delta > 0 else f"down {abs(delta):.2f} percentage points over five observations") if delta is not None else "with insufficient history for a five-observation comparison"
    section["interpretation"] = (f'{latest["above"]} of {latest["eligible"]} eligible GDX constituents ({series["latest"]["close"]:.2f}%) are above their {payload["definition"]["window"]}-day SMA, {direction}. '
                                  f'This describes participation within the fixed {payload["universe"].get("as_of") or "supplied"} holdings universe; it is not historical fund membership or a validated trading signal.')
    section["knowledge_sources"] = ["/sectors/gdx.md", "/references/gdx-breadth.md"]
    section["knowledge_context"] = []
    for relative in section["knowledge_sources"]:
        content = (ROOT / "knowledge" / relative.lstrip("/")).read_text(encoding="utf-8")
        section["knowledge_context"].append({"path": relative, "content": content,
                                              "sha256": hashlib.sha256(content.encode()).hexdigest()})
    report["gdx_breadth"] = section
    report["warnings"].extend(section["warnings"])


def render_html(report: dict) -> str:
    from report_design import render_report
    return render_report(report, chart_svg, breadth_interpretation)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["daily"], nargs="?", default="daily")
    parser.add_argument("--date", type=date.fromisoformat, default=None, help="As-of date YYYY-MM-DD; default today in Stockholm")
    parser.add_argument("--provider", choices=["snapshot", "tradingview", "alpaca"], default="snapshot",
                        help="snapshot reads stored bars; tradingview/alpaca download. Series a provider cannot supply are labelled in the report")
    parser.add_argument("--snapshot", type=Path, help="Optional legacy combined snapshot; default reads the per-symbol bar store")
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--download-date", type=date.fromisoformat, help="Select a stored download batch")
    parser.add_argument("--gdx-breadth", type=Path, default=ROOT / "data/gdx-breadth-sma50.json", help="GDX custom breadth snapshot")
    parser.add_argument("--mcp-url", default=os.environ.get("TRADINGVIEW_MCP_URL", "https://mcp.tradingview.com/mcp"), help="Streamable HTTP MCP endpoint; or TRADINGVIEW_MCP_URL")
    parser.add_argument("--alpaca-feed", choices=["iex", "sip"], default="iex", help="Alpaca feed for --provider alpaca; iex is free but not the consolidated close")
    parser.add_argument("--lookback", type=int, default=6, metavar="MONTHS")
    parser.add_argument("--format", default="html,json", help="html, json, or html,json")
    parser.add_argument("--output", type=Path, default=ROOT / "reports")
    parser.add_argument("--refresh", action="store_true", help="Refresh live-provider cache")
    parser.add_argument("--close-only", action="store_true", help="Exclude today's bar; report previous closes only")
    parser.add_argument("--vix-period", type=int, default=365, help="Maximum closes for VIX day-low metric (default 365 sessions)")
    args = parser.parse_args(argv)
    formats = set(args.format.split(","))
    if not formats or not formats <= {"html", "json"}:
        parser.error("--format must be html, json, or html,json")
    if not 1 <= args.lookback <= 120:
        parser.error("--lookback must be between 1 and 120 months")
    if args.vix_period < 1:
        parser.error("--vix-period must be positive")
    now = datetime.now(NY)
    today = now.date()
    report_today = datetime.now(ZoneInfo("Europe/Stockholm")).date()
    requested = args.date or report_today
    if requested > report_today:
        parser.error("--date cannot be in the future")
    try:
        coverage = []
        report = None
        spy_payload, spy_note, spy_downloads, spy_source = None, None, 0, "unavailable"
        spy_provider = "alpaca" if args.provider == "alpaca" else "tradingview"
        spy_start = requested - timedelta(days=SPY_HISTORY_DAYS)
        batch = args.download_date.isoformat() if args.download_date else None
        vix_downloads = 0
        vix_batch = batch
        if args.provider == "alpaca":
            if args.snapshot or args.refresh:
                parser.error("--snapshot and --refresh do not apply to --provider alpaca")
            availability = {s: provider_availability(s, "alpaca") for s in SYMBOLS}
            if any(a["status"] != "unavailable" for a in availability.values()):
                raise ValueError("Alpaca breadth downloads are not implemented; update the knowledge data_providers entry and the report together")
            # Breadth indices exist only on TradingView: use a stored TradingView
            # batch and label the substitution rather than dropping the section.
            try:
                payload = load_bars(SYMBOLS, args.data_root, provider="tradingview",
                                    download_date=args.download_date.isoformat() if args.download_date else None)
            except ValueError:
                payload = None
            for symbol, a in availability.items():
                coverage.append({"symbol": symbol, "section": "Market breadth", "requested_provider": "alpaca",
                                 "provider_used": "tradingview" if payload else None,
                                 "status": "substituted" if payload else "unavailable",
                                 "reason": a["reason"],
                                 "source": f"stored TradingView batch day/{payload['download_date']}" if payload else None})
            # SPY is a US ETF, so Alpaca supplies it directly; download failures fail the run.
            alpaca_payload = fetch_alpaca_daily(["SPY"], spy_start, observation_cutoff(requested, today, args.close_only) + timedelta(days=1),
                                                feed=args.alpaca_feed)
            alpaca_payload.pop("empty_symbols")
            if alpaca_payload["series"]:
                saved = save_bars(alpaca_payload, args.data_root)
                spy_payload = load_bars(["SPY"], args.data_root, provider="alpaca", download_date=saved[0].parent.name)
                spy_downloads = 1
                spy_source = f"Alpaca ({args.alpaca_feed} feed, fresh)"
            else:
                spy_note = "Alpaca returned no SPY daily bars for the requested window."
            names = "/".join(s.split(":")[1] for s in SYMBOLS)
            if payload:
                source = f"bar store: day/{payload['download_date']} (TradingView; {names} unavailable from Alpaca)"
            else:
                source = "unavailable"
                report = unavailable_report(requested, args.lookback, args.close_only,
                                            f"{names} are not available from Alpaca and no stored TradingView batch was found. "
                                            "Run with --provider tradingview, or download them to the bar store first.")
        elif args.provider == "snapshot":
            if args.refresh:
                parser.error("--refresh requires --provider tradingview")
            payload = read_snapshot(args.snapshot) if args.snapshot else load_bars(SYMBOLS, args.data_root, download_date=args.download_date.isoformat() if args.download_date else None)
            source = f"snapshot: {args.snapshot.name}" if args.snapshot else f"bar store: day/{payload['download_date']}"
            if args.snapshot:
                spy_payload, spy_source = payload, source
            else:
                try:
                    spy_payload = load_bars(["AMEX:SPY"], args.data_root, provider="tradingview", download_date=batch)
                    spy_source = f"bar store: day/{spy_payload['download_date']}"
                except ValueError:
                    spy_note = "No stored TradingView AMEX:SPY history was found; download it to the bar store first."
        else:
            if not args.mcp_url:
                parser.error("--provider tradingview requires --mcp-url or TRADINGVIEW_MCP_URL")
            cache = ROOT / ".cache" / f"tradingview-{requested}-{args.lookback}m.json"
            cached = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() else {}
            # Today's data keeps changing, so only completed days are served from cache.
            if cached.get("bar_store_batch") and not args.refresh and requested < today:
                payload = load_bars(SYMBOLS, args.data_root, download_date=cached["bar_store_batch"])
                source = "TradingView MCP (cached)"
                try:
                    spy_payload = load_bars(["AMEX:SPY"], args.data_root, provider="tradingview", download_date=cached["bar_store_batch"])
                    spy_source = source
                except ValueError:
                    spy_note = "Cached TradingView batch has no AMEX:SPY history; rerun with --refresh."
            else:
                payload = asyncio.run(fetch_tradingview(args.mcp_url, observation_cutoff(requested, today, args.close_only), months_before(requested, args.lookback) - timedelta(days=20)))
                spy_fresh = asyncio.run(fetch_tradingview(args.mcp_url, observation_cutoff(requested, today, args.close_only), spy_start, ("AMEX:SPY",)))
                saved = save_bars(payload, args.data_root)
                save_bars(spy_fresh, args.data_root)
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps({"bar_store_batch": saved[0].parent.name}), encoding="utf-8")
                source = "TradingView MCP (fresh)"
                spy_payload = load_bars(["AMEX:SPY"], args.data_root, provider="tradingview", download_date=saved[0].parent.name)
                spy_source, spy_downloads = source, 1
        if args.provider == "tradingview" and source == "TradingView MCP (fresh)":
            vix_fresh = asyncio.run(fetch_tradingview(args.mcp_url, observation_cutoff(requested, today, args.close_only),
                                                     requested - timedelta(days=max(SPY_HISTORY_DAYS, args.vix_period * 2)), (VIX_SYMBOL,)))
            vix_saved = save_bars(vix_fresh, args.data_root)
            vix_batch, vix_downloads = vix_saved[0].parent.name, 1
        elif args.provider == "tradingview" and cached.get("bar_store_batch"):
            vix_batch = cached["bar_store_batch"]
        try:
            vix_payload = load_bars([VIX_SYMBOL], args.data_root, provider="tradingview", download_date=vix_batch)
        except ValueError:
            vix_payload = None
        if args.provider == "alpaca":
            coverage.append({"symbol": VIX_SYMBOL, "section": "S&P 500", "requested_provider": "alpaca",
                             "provider_used": "tradingview" if vix_payload else None,
                             "status": "substituted" if vix_payload else "unavailable",
                             "reason": "VIX is a spot volatility index, not a US stock or ETF available from Alpaca.",
                             "source": f"stored TradingView batch day/{vix_payload['download_date']}" if vix_payload else None})
        if report is None:
            report = build_report(payload, requested, args.lookback, source, now, args.close_only)
        report["requested_provider"] = None if args.provider == "snapshot" else args.provider
        report["provider_coverage"] = coverage
        report["vix"] = vix_section(vix_payload, requested, args.lookback, now, args.close_only, args.vix_period)
        report["warnings"].extend(report["vix"].get("warnings", []))
        attach_breadth_knowledge(report)
        report["spy"] = spy_section(spy_payload, spy_provider, requested, args.lookback, now, args.close_only,
                                    spy_source if spy_payload else "unavailable", spy_note)
        if "metrics" in report["spy"]:
            report["spy"]["interpretation"] = spy_interpretation(report["spy"])
            report["warnings"].extend(report["spy"]["warnings"])
        attach_gdx_breadth(report, args.gdx_breadth, now, args.close_only)
        report["research_todos"] = collect_research_todos(ROOT / "knowledge")
        fresh_download = args.provider == "tradingview" and source == "TradingView MCP (fresh)"
        data_mode = "Fresh download" if fresh_download else "Stored data"
        if args.provider == "alpaca":
            data_mode = "Alpaca · SPY " + ("downloaded" if spy_downloads else "unavailable") + " · breadth " + ("from stored TradingView data" if payload else "unavailable")
        report["run_status"] = {"downloaded_symbols": (len(payload["series"]) if fresh_download else 0) + spy_downloads + vix_downloads,
                                "data_mode": data_mode,
                                "download_batch": payload.get("download_date") if payload else None}
        args.output.mkdir(parents=True, exist_ok=True)
        for fmt in sorted(formats):
            path = args.output / f"market-report-{requested}.{fmt}"
            content = render_html(report) if fmt == "html" else json.dumps(report, indent=2, allow_nan=False)
            path.write_text(content, encoding="utf-8")
            print(f"Saved {path.resolve()}")
        for symbol, s in report["series"].items():
            print(f'{symbol}: {s["latest"]["close"]:.2f} | daily {change_text(s["daily_change"])} | {s["as_of"]}')
        spy = report["spy"]
        if "metrics" in spy:
            m = spy["metrics"]
            d200 = "n/a" if m["distance_from_sma200_pct"] is None else f'{m["distance_from_sma200_pct"]:+.2f}%'
            print(f'{spy["symbol"]}: {m["close"]:.2f} | vs 200DMA {d200} | above 50DMA {m["cons_days_above_sma50"]} | below 50DMA {m["cons_days_below_sma50"]} | down days {m["cons_down_days"]} | {spy["as_of"]}')
        else:
            print(f'SPY unavailable: {spy["unavailable"]}')
        for item in report["provider_coverage"]:
            used = f'using {item["source"]}' if item["provider_used"] else "not shown"
            print(f'LIMITATION: {item["symbol"]} unavailable from {provider_label(item["requested_provider"])}: {item["reason"]} ({used})')
        if report.get("breadth_unavailable"):
            print(f'LIMITATION: {report["breadth_unavailable"]}')
        for note in report["notes"]:
            print(f"NOTE: {note}")
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
