"""Descriptive stock leadership from dated theme universes and archived bars."""
import hashlib
import math

from bar_store import load_bars, ROOT as DATA_ROOT
from providers import alpaca_symbol
from theme_returns import theme_universes, prices_from_payload, basket_returns, relative_return, metadata


def weighted_rs(values, weights):
    if any(values.get(h) is None for h in weights):
        return None
    if any(not math.isfinite(w) or w < 0 for w in weights.values()) or sum(weights.values()) <= 0:
        raise ValueError("RS weights must be finite, nonnegative, with a positive sum")
    return math.fsum(values[h] * w for h, w in weights.items()) / sum(weights.values())


def closing_high_distance(prices, sessions, period=252):
    """Distance below the highest close over a full trailing session window."""
    window = sessions[-period:]
    if len(window) != period or any(prices.get(d) is None for d in window):
        return None
    high = max(prices[d] for d in window)
    return {"high_close": high, "distance_pct": 100 * (prices[window[-1]] / high - 1),
            "start_date": window[0].isoformat(), "sessions": period}


def build_market_leaders(knowledge, cutoff, *, download_date, provider="tradingview",
                         data_root=DATA_ROOT, symbol_map=None):
    concept = knowledge / "market-leaders.md"
    config = metadata(concept)["market_report"]
    weights = config["weights"]
    proximity_weight = config.get("proximity_weight", 0.2)
    horizons = tuple(weights)
    themes = theme_universes(knowledge, symbol_map, include_extended=True)
    members = {}
    for theme in themes:
        for symbol in theme["symbols"]:
            members.setdefault(symbol, []).append(theme["title"])
    result = {"provider": provider, "download_date": download_date, "weights": weights,
              "proximity_weight": proximity_weight, "high_period": 252,
              "universe_size": len(members), "rows": [], "excluded": [], "input_bar_files": [],
              "used_symbols": [], "as_of": None, "eligible": 0,
              "knowledge_sha256": {}}
    for path in (concept, knowledge / "themes/themes.md", knowledge / "themes/theme-memberships.md"):
        result["knowledge_sha256"][str(path.relative_to(knowledge))] = hashlib.sha256(path.read_bytes()).hexdigest()
    if symbol_map and symbol_map.exists():
        result["symbol_map_sha256"] = hashlib.sha256(symbol_map.read_bytes()).hexdigest()
        result["knowledge_sha256"]["sectors/gdx.md"] = hashlib.sha256((knowledge / "sectors/gdx.md").read_bytes()).hexdigest()
    benchmark = "AMEX:SPY" if provider == "tradingview" else "SPY"
    try:
        if download_date is None:
            raise ValueError("An explicit download batch is required")
        reference = load_bars([benchmark], data_root, download_date=download_date, provider=provider)
        prices = prices_from_payload(reference, [benchmark], cutoff)[benchmark]
        sessions = sorted(d for d, c in prices.items() if c is not None)
        if not sessions:
            raise ValueError("No benchmark sessions")
        end = sessions[-1]
        returns, starts, _ = basket_returns({benchmark: prices}, sessions, end, horizons)
        result.update(as_of=end.isoformat(), start_dates=starts, benchmark=benchmark, benchmark_returns=returns,
                      adjustment=reference.get("adjustment"))
        result["input_bar_files"].extend(reference["bar_files"])
        result["used_symbols"].append(benchmark)
    except ValueError as error:
        result["unavailable"] = str(error)
        result["interpretation"] = "Market leadership is unavailable because the selected batch lacks benchmark history."
        return result
    ranked = []
    for symbol, labels in sorted(members.items()):
        try:
            mapped = symbol if provider == "tradingview" else alpaca_symbol(symbol)
            if mapped is None:
                raise ValueError("Provider does not support this listing")
            payload = load_bars([mapped], data_root, download_date=download_date, provider=provider)
            # Canonical keys preserve corporate-identity cutoffs for both providers.
            canonical = {**payload, "series": {symbol: payload["series"][mapped]}}
            stock_prices = prices_from_payload(canonical, [symbol], end)
            stock_returns, _, reasons = basket_returns(stock_prices, sessions, end, horizons)
            values = {h: relative_return(stock_returns[h], returns[h]) for h in horizons}
            high = closing_high_distance(stock_prices[symbol], sessions)
            if high is None:
                raise ValueError("Incomplete 252-session history for 52W closing-high proximity")
            return_rs = weighted_rs(values, weights)
            score = weighted_rs({**values, "proximity": high["distance_pct"]},
                                {**weights, "proximity": proximity_weight})
            if score is None:
                raise ValueError("Incomplete required history: " + "; ".join(reasons.values() or ["benchmark unavailable"]))
            ranked.append({"symbol": symbol, "themes": sorted(set(labels)), "score": score,
                           "rs": values, "return_rs": return_rs, "high_52w": high,
                           "returns": stock_returns, "fetched_at": payload["fetched_at"]})
            result["input_bar_files"].extend(payload["bar_files"])
            result["used_symbols"].append(mapped)
        except ValueError as error:
            result["excluded"].append({"symbol": symbol, "reason": str(error)})
    ranked.sort(key=lambda row: (-row["score"], row["symbol"]))
    result["eligible"] = len(ranked)
    result["rows"] = [{**row, "rank": i} for i, row in enumerate(ranked[:10], 1)]
    result["interpretation"] = (f'{ranked[0]["symbol"]} leads with a composite score of {ranked[0]["score"]:+.2f} and is {abs(ranked[0]["high_52w"]["distance_pct"]):.1f}% below its 52-week closing high. '
                                if ranked else "No stocks have complete history for all required components. ")
    result["interpretation"] += "The score combines relative price performance versus SPY with a penalty for distance below the high; it is not a validated trading signal."
    return result
