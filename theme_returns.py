"""Core-constituent theme price returns from a single dated bar batch."""
from calendar import monthrange
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml
from bar_store import load_bars, ROOT as DATA_ROOT
from providers import alpaca_symbol

HORIZONS = ("1W", "1M", "3M", "6M", "12M")
US_EXCHANGES = {"NYSE", "NASDAQ", "AMEX"}
# The same tickers previously identified different issuers/businesses. See OKF.
HISTORY_STARTS = {"NASDAQ:SPCX": date(2026, 6, 12), "NASDAQ:PURR": date(2025, 12, 3)}


def metadata(path):
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])


def theme_universes(knowledge: Path, symbol_map: Path | None = None, *, include_extended=False):
    """Read core stock rows only; ETF table and optional extensions are excluded."""
    registry = metadata(knowledge / "themes/themes.md")["themes"]
    result = {t["id"]: {"id": t["id"], "title": t["title"], "symbols": []} for t in registry}
    table = (knowledge / "themes/theme-memberships.md").read_text(encoding="utf-8")
    for line in table.split("# Memberships", 1)[1].split("\n# ", 1)[0].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        roles = {"core universe", "extended candidate"} if include_extended else {"core universe"}
        if len(cells) != 10 or cells[3] not in roles:
            continue
        symbol, theme = cells[:2]
        if theme not in result or symbol.split(":")[0] not in US_EXCHANGES:
            raise ValueError(f"Invalid theme membership: {symbol}, {theme}")
        result[theme]["symbols"].append(symbol)
    # Existing GDX holdings remain authoritative; use its explicit symbol map,
    # filtered to US listings, rather than importing its international basket.
    if "gold-miners" in result and symbol_map and symbol_map.exists():
        mapping = json.loads(symbol_map.read_text(encoding="utf-8"))
        labels = []
        for line in (knowledge / "sectors/gdx.md").read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip("|").split("|")]
            if line.startswith("|") and len(cells) == 3 and "cash" not in cells[1].lower():
                label = cells[0].replace("\\*", "*")
                if label in mapping:
                    labels.append(label)
        result["gold-miners"]["symbols"] = [mapping[s] for s in labels if mapping[s].split(":")[0] in US_EXCHANGES]
    for theme in result.values():
        theme["symbols"] = sorted(set(theme["symbols"]))
    return list(result.values())


def months_before(day, months):
    y, m = divmod(day.year * 12 + day.month - 1 - months, 12)
    return date(y, m + 1, min(day.day, monthrange(y, m + 1)[1]))


def prices_from_payload(payload, symbols, cutoff):
    prices = {}
    for symbol in symbols:
        prices[symbol] = {}
        for bar in payload["series"].get(symbol, []):
            # All eligible listings are US-listed; use their exchange session date.
            zone = ZoneInfo(payload.get("session_timezones", {}).get(symbol, "America/New_York"))
            session = (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=bar["t"])).astimezone(zone).date()
            if session > cutoff or session < HISTORY_STARTS.get(symbol, date.min):
                continue
            close = bar.get("c")
            if close is None:
                prices[symbol][session] = None
            else:
                close = float(close)
                if not math.isfinite(close) or close <= 0:
                    raise ValueError(f"Invalid close for {symbol}")
                prices[symbol][session] = close
    return prices


def basket_returns(prices, sessions, end, horizons=HORIZONS):
    """Daily-rebalanced equal-weight returns; require every stock every session."""
    dates = sorted(d for d in set(sessions) if d <= end)
    output = {h: None for h in horizons}
    starts, reasons = {}, {}
    if not dates or not prices:
        return output, starts, {h: "No eligible history" for h in horizons}
    if end not in dates:
        return output, starts, {h: "No benchmark session at the observation date" for h in horizons}
    for horizon in horizons:
        if horizon == "1W" or horizon.endswith("D"):
            intervals = 5 if horizon == "1W" else int(horizon[:-1])
            start = dates[-intervals - 1] if len(dates) > intervals else None
        else:
            target = months_before(end, int(horizon[:-1]))
            start = next((d for d in reversed(dates) if d <= target), None)
        starts[horizon] = start.isoformat() if start else None
        window = [d for d in dates if start and start <= d <= end]
        if not start or len(window) < 2:
            reasons[horizon] = "Insufficient calendar history"
            continue
        if any(p.get(d) is None for p in prices.values() for d in window):
            reasons[horizon] = "Incomplete constituent history or missing sessions"
            continue
        value = 1.0
        for previous, current in zip(window, window[1:]):
            value *= math.fsum(p[current] / p[previous] for p in prices.values()) / len(prices)
        output[horizon] = 100 * (value - 1)
    return output, starts, reasons


def build_theme_returns(knowledge, cutoff, *, data_root=DATA_ROOT, download_date=None,
                        provider="tradingview", symbol_map=None):
    themes = theme_universes(knowledge, symbol_map)
    result = {"horizons": list(HORIZONS), "provider": provider, "download_date": download_date,
              "rows": [], "input_bar_files": [], "used_symbols": [],
              "method": "Daily-rebalanced equal-weight core-constituent price returns; USD; fixed current membership",
              "knowledge_sha256": {}}
    for path in (knowledge / "themes/themes.md", knowledge / "themes/theme-memberships.md"):
        result["knowledge_sha256"][str(path.relative_to(knowledge))] = hashlib.sha256(path.read_bytes()).hexdigest()
    if symbol_map and symbol_map.exists():
        result["symbol_map_sha256"] = hashlib.sha256(symbol_map.read_bytes()).hexdigest()
        result["knowledge_sha256"]["sectors/gdx.md"] = hashlib.sha256((knowledge / "sectors/gdx.md").read_bytes()).hexdigest()
    # Pin one date for every row; never pick a separate latest batch per theme.
    if download_date is None:
        folders = sorted((data_root / "day").glob("????-??-??"), reverse=True)
        result["download_date"] = download_date = folders[0].name if folders else None
    reference_symbol = "AMEX:SPY" if provider == "tradingview" else "SPY"
    try:
        if download_date is None:
            raise ValueError("No bar batch")
        reference = load_bars([reference_symbol], data_root, download_date=download_date, provider=provider)
        reference_prices = prices_from_payload(reference, [reference_symbol], cutoff)[reference_symbol]
        sessions = sorted(d for d, close in reference_prices.items() if close is not None)
        end = sessions[-1] if sessions else None
        result["input_bar_files"].extend(reference["bar_files"])
        result["used_symbols"].append(reference_symbol)
        fetched = datetime.fromisoformat(reference["fetched_at"].replace("Z", "+00:00")).astimezone(ZoneInfo("America/New_York"))
        result["intraday"] = bool(end and end == fetched.date() and (fetched.hour, fetched.minute) < (16, 0))
    except ValueError:
        sessions, end = [], None
    result["as_of"] = end.isoformat() if end else None
    # 10D supplements the standard horizons for short-term theme comparisons.
    rs_horizons = ("1W", "10D", "1M", "3M", "6M", "12M")
    benchmark = {}
    if end:
        benchmark = basket_returns({reference_symbol: reference_prices}, sessions, end, rs_horizons)[0]
    rs_rows = []
    for theme in themes:
        short_return = None
        row = {**theme, "returns": {h: None for h in HORIZONS}, "eligible": 0,
               "count": len(theme["symbols"]), "reason": None}
        mapped = {s: s if provider == "tradingview" else alpaca_symbol(s) for s in theme["symbols"]}
        if not row["count"]:
            row["reason"] = "No core universe configured"
        elif end is None:
            row["reason"] = "No reference calendar in selected batch"
        elif any(s is None for s in mapped.values()):
            row["reason"] = "Provider cannot supply the full universe"
        else:
            try:
                payload = load_bars(list(mapped.values()), data_root, download_date=download_date, provider=provider)
                raw_prices = prices_from_payload(payload, list(mapped.values()), end)
                prices = {s: raw_prices[t] for s, t in mapped.items()}
                # Apply identity cutoffs to canonical symbols even for Alpaca.
                prices = {s: {d: c for d, c in p.items() if d >= HISTORY_STARTS.get(s, date.min)} for s, p in prices.items()}
                row["eligible"] = sum(p.get(end) is not None for p in prices.values())
                row["returns"], row["start_dates"], row["unavailable"] = basket_returns(prices, sessions, end)
                short_return = basket_returns(prices, sessions, end, ("10D",))[0]["10D"]
                row["fetched_at"] = payload["fetched_at"]
                row["adjustment"] = payload.get("adjustment", "provider split-adjusted price bars")
                result["input_bar_files"].extend(payload["bar_files"])
                result["used_symbols"].extend(mapped.values())
            except ValueError as error:
                row["reason"] = str(error)
        result["rows"].append(row)
        returns = {**row["returns"], "10D": short_return}
        rs_rows.append({"id": row["id"], "title": row["title"],
                        "values": {h: relative_return(returns[h], benchmark.get(h)) for h in rs_horizons}})
    ranked = sorted(rs_rows, key=lambda r: (r["values"]["10D"] is None, -(r["values"]["10D"] or 0), r["title"]))
    valid = [r for r in ranked if r["values"]["10D"] is not None]
    narrative = "No complete 10-session theme comparisons are available."
    if valid:
        narrative = (f'{valid[0]["title"]} leads over 10 sessions ({valid[0]["values"]["10D"]:+.1f}% versus SPY), '
                     f'while {valid[-1]["title"]} is weakest ({valid[-1]["values"]["10D"]:+.1f}%).')
    result["relative_strength"] = {"benchmark": reference_symbol, "horizons": list(rs_horizons),
                                   "benchmark_returns": benchmark, "rows": ranked,
                                   "interpretation": narrative + " Positive values indicate market outperformance; compare rows to identify stronger and weaker themes, with overlapping memberships limiting independence."}
    result["input_bar_files"] = list({(p["symbol"], p["file"]): p for p in result["input_bar_files"]}.values())
    result["used_symbols"] = sorted(set(result["used_symbols"]))
    available = [r for r in result["rows"] if r["returns"]["1M"] is not None]
    if available:
        leader, laggard = max(available, key=lambda r: r["returns"]["1M"]), min(available, key=lambda r: r["returns"]["1M"])
        result["interpretation"] = f'{leader["title"]} leads the available baskets over 1M ({leader["returns"]["1M"]:+.1f}%), while {laggard["title"]} has the lowest return ({laggard["returns"]["1M"]:+.1f}%). '
    else:
        result["interpretation"] = "No complete one-month theme baskets are available in the selected batch. "
    result["interpretation"] += "These fixed current-universe price returns exclude dividends; overlapping memberships and incomplete histories limit comparisons."
    return result


def relative_return(theme_return, benchmark_return):
    """Percentage change of the theme/benchmark price ratio over one horizon."""
    if theme_return is None or benchmark_return is None:
        return None
    if benchmark_return <= -100:
        raise ValueError("Benchmark price return must exceed -100%")
    return 100 * ((1 + theme_return / 100) / (1 + benchmark_return / 100) - 1)
