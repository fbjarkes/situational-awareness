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
from zoneinfo import ZoneInfo

import knowledge

ROOT = Path(__file__).resolve().parent
SYMBOLS = ("INDEX:MMOH", "INDEX:MMOF")
SECTIONS = {"breadth": {"title": "Market breadth", "symbols": SYMBOLS}}
COLORS = ("#55d6be", "#ffbf69")
NY = ZoneInfo("America/New_York")
MARKET_CLOSE = time(16, 0)


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


def observation_cutoff(requested: date, today: date, close_only: bool) -> date:
    return min(requested, today - timedelta(days=1)) if close_only else requested


def build_report(payload: dict, requested: date, lookback: int, source: str,
                 now: datetime | None = None, close_only: bool = False) -> dict:
    now = (now or datetime.now(NY)).astimezone(NY)
    today = now.date()
    cutoff = observation_cutoff(requested, today, close_only)
    # A bar dated on the fetch day, fetched before 16:00 ET, is still forming.
    fetched = payload.get("fetched_at")
    fetched_ny = datetime.fromisoformat(fetched.replace("Z", "+00:00")).astimezone(NY) if fetched else now
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
        intraday = date.fromisoformat(latest["date"]) == fetched_ny.date() and fetched_ny.time() < MARKET_CLOSE
        as_of = (f"intraday {latest['date']} {fetched_ny:%H:%M} ET" if intraday else f"close {latest['date']}")
        series[symbol] = {"latest": latest, "previous": previous, "latest_status": "intraday" if intraday else "close", "as_of": as_of,
                          "daily_change": round(latest["close"] - previous["close"], 4) if previous else None,
                          "five_session_change": round(latest["close"] - fifth["close"], 4) if fifth else None,
                          "observations": visible}
    mixed = len({s["as_of"] for s in series.values()}) > 1
    notes = ["Readings come from different dates or times; each line below says which."] if mixed else []
    for symbol, s in series.items():
        name = symbol.split(":")[1]
        if s["latest_status"] == "intraday":
            notes.append(f"{name}: today's intraday reading as of {fetched_ny:%H:%M} ET; not a closing value. "
                         "Changes compare it with the previous close.")
        elif mixed or (requested == today and s["latest"]["date"] < requested.isoformat()):
            notes.append(f"{name}: using the {s['latest']['date']} close; no newer reading was available.")
    return {"schema_version": 1, "title": "Daily situational awareness · Market breadth",
            "requested_date": requested.isoformat(), "observation_cutoff": cutoff.isoformat(),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "provider": payload["provider"], "data_fetched_at": payload.get("fetched_at"),
            "source": source, "lookback_months": lookback, "warnings": warnings, "notes": notes,
            "daily_bar_policy": ("Exclude the current New York calendar date." if close_only else
                                 "Include today's bar when available; label it intraday if fetched before 16:00 ET."),
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


def attach_knowledge(report: dict, concepts: dict[str, dict]) -> dict:
    """Add each section's retrieved knowledge and a direction-only fallback interpretation."""
    report["sections"] = {}
    for name, section in SECTIONS.items():
        report["sections"][name] = {
            "title": section["title"], "symbols": list(section["symbols"]),
            "knowledge": knowledge.retrieve(concepts, name, section["symbols"]),
            "interpretation": {"method": "direction-only", "text": breadth_interpretation(report), "sources": []},
        }
    return report


def apply_interpretations(report: dict, supplied: dict, concepts: dict[str, dict]) -> dict:
    """Replace fallback text with interpretations written from retrieved knowledge."""
    if supplied.get("requested_date") != report["requested_date"]:
        raise ValueError(f"Interpretations are for {supplied.get('requested_date')}, report is {report['requested_date']}")
    for name, entry in (supplied.get("sections") or {}).items():
        if name not in report["sections"]:
            raise ValueError(f"Unknown report section in interpretations: {name}")
        text = str(entry.get("text") or "").strip()
        if not text:
            raise ValueError(f"Interpretation for {name} is empty")
        sources = list(entry.get("sources") or [])
        unknown = [path for path in sources if path not in concepts]
        if unknown:
            raise ValueError(f"Interpretation for {name} cites unknown knowledge paths: {', '.join(unknown)}")
        report["sections"][name]["interpretation"] = {"method": "knowledge-retrieval", "text": text, "sources": sources}
    return report


def context_markdown(report: dict, concepts: dict[str, dict], interpretations_path: Path) -> str:
    """Facts plus full retrieved concepts, for an agent writing knowledge-based interpretations."""
    lines = [f"# Market context {report['requested_date']}", "",
             "Write interpretations following \"Interpreting readings with the knowledge bundle\" in AGENTS.md.",
             f"Save them as JSON to `{interpretations_path}`:", "", "```json",
             json.dumps({"requested_date": report["requested_date"],
                         "sections": {name: {"text": "One or two sentences.", "sources": ["/bundle/path.md"]}
                                      for name in report["sections"]}}, indent=2),
             "```", "", "Then run `uv run market-report.py render --report "
             f"{interpretations_path.parent / ('market-report-' + report['requested_date'] + '.json')} "
             f"--interpretations {interpretations_path}`.", ""]
    for name, section in report["sections"].items():
        lines += [f"## Section: {name}", "", "### Readings", ""]
        for symbol in section["symbols"]:
            s = report["series"][symbol]
            previous = f'{s["previous"]["close"]:.2f} on {s["previous"]["date"]}' if s["previous"] else "unavailable"
            recent = ", ".join(f'{b["date"]} {b["close"]:.2f}' for b in s["observations"][-10:])
            lines += [f'- {symbol}: {s["latest"]["close"]:.2f} ({s["as_of"]}); previous close {previous}; '
                      f'daily {change_text(s["daily_change"])}; five-session {change_text(s["five_session_change"])}',
                      f"  Recent closes: {recent}"]
        lines += ["", "### Notes and warnings", ""]
        lines += [f"- {n}" for n in report["notes"] + report["warnings"]] or ["- None"]
        lines += ["", "### Retrieved knowledge", ""]
        for item in section["knowledge"]:
            lines += [f'#### {item["path"]} ({item["relation"]}; {item["type"]}; status {item["status"]}; '
                      f'evidence {item["evidence_status"]}; enabled {item["enabled"]})', "",
                      concepts[item["path"]]["text"].strip(), ""]
    return "\n".join(lines)


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
    if any(s["latest_status"] == "intraday" for s in series):
        recap += " Today's values are intraday and can change before the close."
    return recap


def render_section(title: str, visual: str, interpretation: str) -> str:
    """Shared report template: one chart or table followed by a brief interpretation."""
    return f'<section class="section"><h2>{escape(title)}</h2>{visual}<p class="interpretation">{escape(interpretation)}</p></section>'


def render_html(report: dict) -> str:
    legend = "".join(
        f'<span style="color:{color}">{symbol.split(":")[1]} {report["series"][symbol]["latest"]["close"]:.2f} '
        f'<small>({escape(report["series"][symbol]["as_of"])})</small></span>'
        for symbol, color in zip(SYMBOLS, COLORS)
    )
    visual = f'<div class="legend">{legend}</div>{chart_svg(report)}<small>TradingView · {report["lookback_months"]}-month view</small>'
    breadth = report["sections"]["breadth"]
    section = render_section(breadth["title"], visual, breadth["interpretation"]["text"])
    warnings = "".join(f'<p class="warning">{escape(w)}</p>' for w in report["warnings"])
    warnings += "".join(f'<p class="note">{escape(n)}</p>' for n in report["notes"])
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Market report · {report['requested_date']}</title>
<style>body{{background:#0b1220;color:#e4edf8;font:16px system-ui;margin:0}}main{{max-width:1000px;margin:auto;padding:32px 24px}}h1{{font-size:24px;font-weight:500;margin-bottom:32px}}h1 small{{font-size:14px;color:#aebed1}}h2{{font-size:20px;margin:0 0 20px}}.section{{margin-bottom:40px}}svg{{width:100%;height:auto}}svg text{{fill:#aebed1;font-size:12px}}.legend{{display:flex;gap:24px;font-size:14px}}small{{color:#aebed1;font-size:12px}}.interpretation{{line-height:1.65;max-width:85ch}}.warning{{background:#4c3617;padding:12px;border-radius:8px}}.note{{background:#17324c;padding:12px;border-radius:8px}}</style>
<main><h1>Daily situational awareness <small>{report['requested_date']}</small></h1>{warnings}{section}</main></html>'''


def write_outputs(report: dict, folder: Path, formats: set[str]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for fmt in sorted(formats):
        path = folder / f"market-report-{report['requested_date']}.{fmt}"
        content = render_html(report) if fmt == "html" else json.dumps(report, indent=2, allow_nan=False)
        path.write_text(content, encoding="utf-8")
        print(f"Saved {path.resolve()}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["daily", "render"], nargs="?", default="daily",
                        help="daily: fetch data and build the report; render: apply interpretations to a saved report")
    parser.add_argument("--date", type=date.fromisoformat, default=None, help="As-of date YYYY-MM-DD; default today in New York")
    parser.add_argument("--provider", choices=["snapshot", "tradingview"], default="snapshot")
    parser.add_argument("--snapshot", type=Path, default=ROOT / "data/tradingview-breadth.json")
    parser.add_argument("--mcp-url", default=os.environ.get("TRADINGVIEW_MCP_URL", "https://mcp.tradingview.com/mcp"), help="Streamable HTTP MCP endpoint; or TRADINGVIEW_MCP_URL")
    parser.add_argument("--lookback", type=int, default=6, metavar="MONTHS")
    parser.add_argument("--format", default="html,json", help="html, json, or html,json")
    parser.add_argument("--output", type=Path, default=ROOT / "reports")
    parser.add_argument("--refresh", action="store_true", help="Refresh live-provider cache")
    parser.add_argument("--close-only", action="store_true", help="Exclude today's bar; report previous closes only")
    parser.add_argument("--context", action="store_true", help="daily: also write a context file for an interpreting agent")
    parser.add_argument("--knowledge", type=Path, default=knowledge.ROOT, help="OKF knowledge bundle directory")
    parser.add_argument("--report", type=Path, help="render: saved report JSON")
    parser.add_argument("--interpretations", type=Path, help="render: interpretations JSON")
    args = parser.parse_args(argv)
    formats = set(args.format.split(","))
    if not formats or not formats <= {"html", "json"}:
        parser.error("--format must be html, json, or html,json")
    if not 1 <= args.lookback <= 120:
        parser.error("--lookback must be between 1 and 120 months")
    if args.command == "render":
        if not args.report or not args.interpretations:
            parser.error("render requires --report and --interpretations")
        try:
            report = json.loads(args.report.read_text(encoding="utf-8"))
            supplied = json.loads(args.interpretations.read_text(encoding="utf-8"))
            apply_interpretations(report, supplied, knowledge.load_concepts(args.knowledge))
            write_outputs(report, args.report.parent, formats)
            return 0
        except (OSError, ValueError, KeyError, TypeError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    if args.report or args.interpretations:
        parser.error("--report and --interpretations are only used with render")
    now = datetime.now(NY)
    today = now.date()
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
            # Today's data keeps changing, so only completed days are served from cache.
            if cache.exists() and not args.refresh and requested < today:
                payload = read_snapshot(cache)
                source = "TradingView MCP (cached)"
            else:
                payload = asyncio.run(fetch_tradingview(args.mcp_url, observation_cutoff(requested, today, args.close_only), months_before(requested, args.lookback) - timedelta(days=20)))
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps(payload, indent=2), encoding="utf-8")
                source = "TradingView MCP (fresh)"
        report = build_report(payload, requested, args.lookback, source, now, args.close_only)
        concepts = knowledge.load_concepts(args.knowledge)
        attach_knowledge(report, concepts)
        write_outputs(report, args.output, formats)
        if args.context:
            context = args.output / f"market-context-{requested}.md"
            interpretations = args.output / f"market-interpretations-{requested}.json"
            context.write_text(context_markdown(report, concepts, interpretations), encoding="utf-8")
            print(f"Saved {context.resolve()}")
        for symbol, s in report["series"].items():
            print(f'{symbol}: {s["latest"]["close"]:.2f} | daily {change_text(s["daily_change"])} | {s["as_of"]}')
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
