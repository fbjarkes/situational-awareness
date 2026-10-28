"""Provider-independent daily price statistics.

Every function takes daily closes ordered oldest to newest and describes the
latest close. Moving averages are simple and include the current close, as
in breadth.py. Streaks count sessions ending at the latest close; a streak
that reaches the start of the supplied history is a lower bound.
"""
from __future__ import annotations

from collections.abc import Sequence
import math

KMA_PERIODS = (5, 10, 20, 50, 100, 150, 200)


def kma_compression(closes: Sequence[float], periods: Sequence[int] = KMA_PERIODS) -> float | None:
    """SMA range as percent of latest close: 100 * (max(SMAs)-min(SMAs))/close.

    Lower means tighter compression; zero means all averages coincide.
    Requires every requested SMA; returns None without full warmup.
    """
    values = _validate(closes)
    windows = [_period(p) for p in periods]
    if len(set(windows)) < 2 or len(set(windows)) != len(windows):
        raise ValueError("Provide at least two distinct moving-average periods")
    if len(values) < max(windows):
        return None
    averages = [math.fsum(values[-p:]) / p for p in windows]
    return 100 * (max(averages) - min(averages)) / values[-1]


def new_52w_high(prices: Sequence[float], period: int = 252) -> bool | None:
    """Whether latest price strictly exceeds the preceding `period` prices.

    52 weeks is approximated by 252 trading sessions, excluding today.
    Pass daily highs for intraday-high research, closes for closing highs.
    Ties return False; insufficient history returns None.
    """
    values, period = _validate(prices), _period(period)
    if len(values) <= period:
        return None
    return values[-1] > max(values[-period - 1:-1])


def days_since_52w_high(prices: Sequence[float], period: int = 252) -> int | None:
    """Sessions since the most recent strict rolling-high event; today is zero.

    Each event must exceed its own preceding `period` observations. Returns
    None if no fully warmed-up event exists in the supplied history; this
    differs from the age of the maximum in today's trailing window.
    """
    values, period = _validate(prices), _period(period)
    for i in range(len(values) - 1, period - 1, -1):
        if values[i] > max(values[i - period:i]):
            return len(values) - 1 - i
    return None


def _validate(closes: Sequence[float]) -> list[float]:
    values = [float(c) for c in closes]
    if any(not math.isfinite(c) or c <= 0 for c in values):
        raise ValueError("Closes must be positive finite numbers")
    return values


def _period(period: int) -> int:
    if isinstance(period, bool) or not isinstance(period, int) or period < 1:
        raise ValueError("period must be a positive integer")
    return period


def sma(closes: Sequence[float], period: int) -> float | None:
    """Simple average of the latest `period` closes, or None with less history."""
    values, period = _validate(closes), _period(period)
    return math.fsum(values[-period:]) / period if len(values) >= period else None


def distance_from_ma(closes: Sequence[float], period: int) -> float | None:
    """Latest close relative to its SMA, in percent: 100 * (close / SMA - 1)."""
    average = sma(closes, period)
    return None if average is None else 100 * (float(closes[-1]) / average - 1)


def cons_down_days(closes: Sequence[float]) -> int:
    """Consecutive sessions ending today with a close strictly below the previous close."""
    values = _validate(closes)
    count = 0
    for i in range(len(values) - 1, 0, -1):
        if values[i] >= values[i - 1]:
            break
        count += 1
    return count


def cons_up_days(closes: Sequence[float]) -> int:
    """Consecutive sessions ending today with a close strictly above the previous close."""
    return cons_down_days([1 / c for c in _validate(closes)]) if closes else 0


def _ma_streak(closes: Sequence[float], period: int, above: bool) -> int:
    values, period = _validate(closes), _period(period)
    count = 0
    # Walk back while each session's close is strictly on the requested side
    # of the SMA ending on that same session.
    for end in range(len(values), period - 1, -1):
        average = math.fsum(values[end - period:end]) / period
        close = values[end - 1]
        if math.isclose(close, average, rel_tol=1e-12) or (close > average) != above:
            break
        count += 1
    return count


def cons_days_above_ma(closes: Sequence[float], period: int) -> int:
    """Consecutive sessions ending today with the close strictly above its SMA."""
    return _ma_streak(closes, period, above=True)


def cons_days_below_ma(closes: Sequence[float], period: int) -> int:
    """Consecutive sessions ending today with the close strictly below its SMA."""
    return _ma_streak(closes, period, above=False)


def streak_is_lower_bound(closes: Sequence[float], streak: int, period: int = 1) -> bool:
    """True when a streak reaches the earliest evaluable session, so it may be longer."""
    evaluable = len(closes) - period + 1 if period > 1 else len(closes) - 1
    return streak > 0 and streak >= evaluable


def lowest_close_period(closes: Sequence[float], period: int | None = None) -> int:
    """Longest trailing window where the latest close is a strict new low.

    Includes the latest observation: [12, 11, 10] -> 3; [10, 12, 11] -> 2.
    A higher/equal latest close, or fewer than two observations, returns zero.
    `period` caps the window including the latest observation; None uses all.
    """
    values = _validate(closes)
    if period is not None:
        values = values[-_period(period):]
    if len(values) < 2 or values[-1] >= values[-2]:
        return 0
    count = 1
    for previous in reversed(values[:-1]):
        if previous <= values[-1]:
            break
        count += 1
    return count
