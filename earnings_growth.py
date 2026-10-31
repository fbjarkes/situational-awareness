"""Year-on-year quarterly growth from cached financials, retaining label uncertainty."""
from collections import Counter
import hashlib
import json
import math
import re

from earnings import ROOT, cache_path


def quarter_number(label):
    match = re.fullmatch(r"Q([1-4]) (\d{4})", label)
    return int(match[2]) * 4 + int(match[1]) - 1 if match else None


def growth_pct(current, previous):
    """Ordinary percentage growth; a nonpositive base is not meaningful."""
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
           for v in (current, previous)) or previous <= 0:
        return None
    return 100 * (current / previous - 1)


def quarterly_growth(quarters):
    counts = Counter(row["period_label"] for row in quarters)
    by_quarter = {quarter_number(row["period_label"]): row for row in quarters}
    result = []
    for i, row in enumerate(quarters):
        label = row["period_label"]
        current_number = quarter_number(label)
        previous = by_quarter.get(current_number - 4) if current_number is not None else None
        reason = None
        if counts[label] > 1 or (previous and counts[previous["period_label"]] > 1):
            reason = "Ambiguous duplicate quarter label"
        elif current_number is None or previous is None:
            reason = "Same quarter of the prior year is unavailable"
        values = {metric: growth_pct(row.get(metric), previous.get(metric)) if not reason else None
                  for metric in ("revenue", "eps")}
        result.append({"period_label": label, "provider_index": row.get("provider_index", i),
                       "revenue": row.get("revenue"), "eps": row.get("eps"),
                       "comparison_period": previous["period_label"] if previous else None,
                       "revenue_yoy_pct": values["revenue"], "eps_yoy_pct": values["eps"],
                       "reason": reason,
                       "metric_notes": {metric: "Missing value or nonpositive prior value" for metric, value in values.items()
                                        if value is None and not reason}})
    return result


def build_earnings_growth(symbols, *, data_root=ROOT):
    result = {"provider": "tradingview", "rows": [], "input_files": [],
              "universe": "Current top 10 Market Leaders", "available": 0}
    for symbol in dict.fromkeys(symbols):
        row = {"symbol": symbol, "quarters": [], "warnings": []}
        path = cache_path(symbol, data_root)
        try:
            raw = path.read_bytes()
            cached = json.loads(raw)
            if (cached.get("provider") != "tradingview" or cached.get("symbol") != symbol
                    or cached.get("period") != "fq" or not cached.get("quarters")):
                raise ValueError("Invalid quarterly earnings cache")
            row["quarters"] = list(reversed(quarterly_growth(cached["quarters"])))
            row["warnings"] = cached.get("warnings", [])
            row["fetched_at"] = cached["fetched_at"]
            row["request"] = cached["request"]
            row["currency"] = cached.get("currency")
            row["eps_basis"] = cached.get("eps_basis")
            result["available"] += 1
            result["input_files"].append({"symbol": symbol, "file": str(path), "sha256": hashlib.sha256(raw).hexdigest()})
        except (OSError, ValueError, KeyError, TypeError):
            row["unavailable"] = "Quarterly earnings cache is missing or invalid"
        result["rows"].append(row)
    result["columns"] = max((len(row["quarters"]) for row in result["rows"]), default=0)
    comparable = [q for row in result["rows"] for q in row["quarters"][:1]
                  if q["revenue_yoy_pct"] is not None and q["eps_yoy_pct"] is not None]
    growing = sum(q["revenue_yoy_pct"] > 0 and q["eps_yoy_pct"] > 0 for q in comparable)
    result["interpretation"] = (f'{growing} of {len(comparable)} companies with comparable latest quarters show both revenue and EPS growth YoY. '
                                if comparable else "No companies have an unambiguous latest-quarter comparison for both metrics. ")
    result["interpretation"] += "Quarter labels are preserved as provided; duplicate labels, gaps and nonpositive prior values leave growth unavailable."
    return result
