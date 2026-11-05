"""Weekly derived studies; daily reports only read their saved snapshots."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from situational_awareness.bar_store import load_bars
from situational_awareness.breadth import calculate_breadth
from situational_awareness.providers import alpaca_symbol
from situational_awareness.theme_returns import theme_universes, metadata, prices_from_payload


def update_gdx_breadth(*, weekly, knowledge, symbol_map, output, data_root, provider, cutoff, download_date=None):
    """Rebuild US-listed GDX breadth only when explicitly running weekly.

    Raw bars are shared with the daily gold-miners theme. Never download foreign
    listings or replace the fixed US subset with a mixed international denominator.
    """
    if not weekly:
        return {"status": "reused", "updated": False}
    themes = theme_universes(Path(knowledge), Path(symbol_map))
    symbols = next(t["symbols"] for t in themes if t["id"] == "gold-miners")
    if not symbols:
        raise ValueError("No US-listed GDX constituents configured")
    stored_symbols = symbols if provider == "tradingview" else [alpaca_symbol(s) for s in symbols]
    source = load_bars(stored_symbols, data_root, provider=provider, download_date=download_date)
    by_symbol = prices_from_payload(source, stored_symbols, cutoff)
    prices = {s: {d.isoformat(): c for d, c in by_symbol[stored].items()} for s, stored in zip(symbols, stored_symbols)}
    holdings = metadata(Path(knowledge) / "sectors/gdx.md").get("holdings_snapshot", {})
    snapshot = calculate_breadth(symbols, prices, 50, end=cutoff, min_coverage=.8,
                                name="CUSTOM:GDX-US-SMA50", universe_as_of=holdings.get("as_of"))
    snapshot.update(cadence="weekly", universe_scope="US-listed GDX constituents only",
                    updated_at=datetime.now(timezone.utc).isoformat(), input_provider=provider,
                    input_fetched_at=source["fetched_at"], input_bar_files=source["bar_files"],
                    input_download_date=source["download_date"],
                    input_sha256=hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest())
    snapshot["universe"]["selection_policy"] = "US-listed subset of fixed GDX holdings; foreign listings excluded from denominator"
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, indent=2, allow_nan=False), encoding="utf-8")
    return {"status": "refreshed", "updated": True, "symbols": len(symbols), "download_date": source["download_date"]}
