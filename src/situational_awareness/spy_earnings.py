"""Screen the recorded SPY holdings for two latest quarters of >25% revenue YoY."""
import hashlib
import json
import re

from situational_awareness.earnings import ROOT as EARNINGS_ROOT
from situational_awareness.earnings_growth import build_earnings_growth, quarter_number
from situational_awareness.theme_returns import metadata


def spy_holdings(path):
    """Numbered security rows only; excludes cash and the non-standard entry."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|([^|]+)\|", line)
        if match:
            rows.append({"ticker": match[1], "company": match[2].strip()})
    if not rows or len({row["ticker"] for row in rows}) != len(rows):
        raise ValueError("Holdings must contain unique numbered security tickers")
    return rows


def revenue_streak(quarters, threshold=25):
    """None means unassessable, False means assessed but not passing."""
    if len(quarters) < 2:
        return None
    latest, previous = quarters[:2]  # Growth rows are newest first.
    numbers = [quarter_number(q["period_label"]) for q in (latest, previous)]
    if None in numbers or numbers[0] != numbers[1] + 1:
        return None
    values = [q["revenue_yoy_pct"] for q in (latest, previous)]
    if any(value is None for value in values):
        return None
    return all(value > threshold for value in values)


def build_spy_revenue_screen(holdings_path, symbol_map, *, data_root=EARNINGS_ROOT, threshold=25):
    holdings = spy_holdings(holdings_path)
    result = {"provider": "tradingview", "threshold_pct": threshold, "universe_size": len(holdings),
              "holdings_as_of": str(metadata(holdings_path)["holdings_snapshot"]["as_of"]),
              "universe": "Recorded SPY holdings; latest two reported quarters with revenue YoY > 25%",
              "holdings_sha256": hashlib.sha256(holdings_path.read_bytes()).hexdigest(),
              "rows": [], "excluded": [], "input_files": [], "available": 0, "assessable": 0, "columns": 0}
    if not symbol_map.exists():
        result["interpretation"] = "The SPY revenue screen is unavailable because its symbol map is missing."
        return result
    mapping = json.loads(symbol_map.read_text(encoding="utf-8"))["symbols"]
    result["symbol_map_sha256"] = hashlib.sha256(symbol_map.read_bytes()).hexdigest()
    symbols = [mapping[row["ticker"]] for row in holdings if row["ticker"] in mapping]
    growth = build_earnings_growth(symbols, data_root=data_root)
    result["available"] = growth["available"]
    result["input_files"] = growth["input_files"]
    by_symbol = {row["symbol"]: row for row in growth["rows"]}
    for holding in holdings:
        symbol = mapping.get(holding["ticker"])
        row = by_symbol.get(symbol)
        passes = revenue_streak(row["quarters"], threshold) if row else None
        if passes is None:
            reason = "Missing symbol mapping" if not row else row.get("unavailable")
            if row and not reason:
                reasons = [q.get("reason") or q.get("metric_notes", {}).get("revenue") for q in row["quarters"][:2]]
                reason = next((r for r in reasons if r), "Latest two reported quarters are not consecutive or unavailable")
            result["excluded"].append({**holding, "symbol": symbol,
                                       "reason": reason})
        else:
            result["assessable"] += 1
            if passes:
                result["rows"].append({**row, "company": holding["company"]})
    result["rows"].sort(key=lambda r: (-min(q["revenue_yoy_pct"] for q in r["quarters"][:2]), r["symbol"]))
    result["columns"] = max((len(row["quarters"]) for row in result["rows"]), default=0)
    result["interpretation"] = (f'{len(result["rows"])} of {result["assessable"]} assessable SPY holdings have revenue growth above {threshold:g}% YoY in each of their latest two consecutive quarters. '
                                f'{len(result["excluded"])} holdings lack sufficient unambiguous comparisons; this screen uses the recorded holdings snapshot and current cached financials.')
    return result
