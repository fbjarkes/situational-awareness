"""Provider-independent, equal-weight breadth from daily closing prices."""
from collections import deque
from datetime import date, datetime, timezone
import math
from collections.abc import Mapping, Sequence


def calculate_breadth(
    symbols: Sequence[str], prices: Mapping[str, Mapping[str, float | None]],
    window: int = 50, *, start: date | str | None = None,
    end: date | str | None = None, min_coverage: float = 0.0,
    name: str | None = None, universe_as_of: str | None = None,
) -> dict:
    """Return a snapshot from {symbol: {ISO date: close}} daily histories.

    SMA includes the current close and requires `window` valid observations.
    Pass full histories: date filtering happens after warmup. Missing sessions
    are never forward-filled. Symbols without a current close/full SMA are
    excluded from that day's denominator, with coverage recorded explicitly.
    """
    symbols = list(dict.fromkeys(symbols))
    if not symbols or any(not isinstance(s, str) or not s.strip() for s in symbols):
        raise ValueError("Provide at least one nonempty symbol")
    if isinstance(window, bool) or not isinstance(window, int) or window < 1:
        raise ValueError("window must be a positive integer")
    if not 0 <= min_coverage <= 1:
        raise ValueError("min_coverage must be between 0 and 1")
    start = date.fromisoformat(start) if isinstance(start, str) else start
    end = date.fromisoformat(end) if isinstance(end, str) else end
    if start and end and start > end:
        raise ValueError("start must not be after end")
    daily = {}
    missing_symbols = []
    for symbol in symbols:
        history = prices.get(symbol, {})
        if not history:
            missing_symbols.append(symbol)
        rolling = deque(maxlen=window)
        for day, close in sorted(history.items()):
            observed = date.fromisoformat(day)
            if end and observed > end:
                break
            record = daily.setdefault(observed, {"above": 0, "below": 0, "equal": 0})
            if close is None:
                rolling.clear()
                continue
            if isinstance(close, bool) or not isinstance(close, (int, float)) or not math.isfinite(close) or close <= 0:
                raise ValueError(f"Invalid closing price for {symbol} on {day}")
            rolling.append(float(close))
            if len(rolling) == window:
                average = math.fsum(rolling) / window
                category = "equal" if math.isclose(close, average, rel_tol=1e-12) else "above" if close > average else "below"
                record[category] += 1
    bars = []
    for day, counts in sorted(daily.items()):
        if start and day < start:
            continue
        eligible = sum(counts.values())
        coverage = eligible / len(symbols)
        usable = eligible > 0 and coverage >= min_coverage
        bars.append({"t": int(datetime.combine(day, datetime.min.time(), timezone.utc).timestamp()),
                     "o": None, "h": None, "l": None, "c": 100 * counts["above"] / eligible if usable else None,
                     "v": None, **counts, "eligible": eligible, "universe_size": len(symbols),
                     "unavailable": len(symbols) - eligible, "coverage": coverage,
                     "below_pct": 100 * counts["below"] / eligible if usable else None,
                     "equal_pct": 100 * counts["equal"] / eligible if usable else None})
    if not bars:
        raise ValueError("No daily observations in the requested period")
    series_name = name or f"CUSTOM:BREADTH-SMA{window}"
    return {"schema_version": 1, "provider": "custom-breadth",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "definition": {"average": "SMA", "window": window, "includes_current_close": True,
                           "weighting": "equal", "close_units": "percent_above",
                           "min_coverage": min_coverage, "missing_policy": "no forward fill; exclude ineligible symbols",
                           "null_close_policy": "reset SMA warmup", "timestamps": "UTC midnight session date",
                           "ohlc_policy": "close-only derived series; open/high/low/volume unavailable"},
            "universe": {"symbols": symbols, "as_of": universe_as_of,
                         "membership_policy": "fixed supplied universe, not historical membership",
                         "missing_symbols": missing_symbols},
            "series": {series_name: bars}}
