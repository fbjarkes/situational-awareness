"""Dated, per-symbol raw bar storage shared by reports and research utilities."""
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent / "data/research"


def symbol_filename(symbol: str) -> str:
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("Symbol must be a nonempty string")
    # Percent encoding is reversible, collision-free, and safe on Windows.
    return quote(symbol, safe="") + ".json"


def download_day(fetched_at: str) -> str:
    instant = datetime.fromisoformat(fetched_at.replace("Z", "+00:00"))
    if instant.tzinfo is None:
        raise ValueError("fetched_at must include a timezone")
    return instant.astimezone(ZoneInfo("Europe/Stockholm")).date().isoformat()


def save_bars(payload: dict, root: Path = ROOT, *, timeframe: str = "day") -> list[Path]:
    """Archive one file per symbol, retaining existing history on same-day refreshes."""
    if timeframe != "day":
        raise ValueError("Only daily bar storage is supported currently")
    fetched = payload["fetched_at"]
    folder = Path(root) / timeframe / download_day(fetched)
    folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for symbol, bars in payload["series"].items():
        if not bars:
            raise ValueError(f"Cannot archive an empty history for {symbol}")
        path = folder / symbol_filename(symbol)
        saved = {k: v for k, v in payload.items() if k not in ("series", "symbol_resolution")}
        saved.update({"schema_version": 1, "timeframe": timeframe, "symbol": symbol,
                      "download_date": folder.name})
        history = {}
        retrievals = []
        retrieval = {"fetched_at": fetched, "first_t": min(b["t"] for b in bars),
                     "last_t": max(b["t"] for b in bars), "count": len(bars)}
        if path.exists():
            old = json.loads(path.read_text(encoding="utf-8"))
            if old.get("provider") != payload.get("provider"):
                raise ValueError(f"Provider conflict for {path.name}")
            history = {b["t"]: b for b in old["series"][symbol]}
            retrievals = old.get("retrievals", [])
            incoming = datetime.fromisoformat(fetched.replace("Z", "+00:00"))
            existing = datetime.fromisoformat(old["fetched_at"].replace("Z", "+00:00"))
            if existing > incoming:
                # An older full-history import may fill gaps, but must not undo
                # more recently retrieved values or their fetch timestamp.
                bars = [b for b in bars if b["t"] not in history]
                saved["fetched_at"] = old["fetched_at"]
        retrievals.append(retrieval)
        history.update({b["t"]: b for b in bars})
        saved["series"] = {symbol: [history[t] for t in sorted(history)]}
        saved["retrievals"] = retrievals
        temp = path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(saved, allow_nan=False), encoding="utf-8")
        temp.replace(path)
        paths.append(path)
    return paths


def load_bars(symbols, root: Path = ROOT, *, download_date: str | None = None,
              timeframe: str = "day") -> dict:
    """Read the latest complete dated batch; never silently mix download dates."""
    if timeframe != "day":
        raise ValueError("Only daily bar storage is supported currently")
    symbols = list(dict.fromkeys(symbols))
    if not symbols:
        raise ValueError("At least one symbol is required")
    base = Path(root) / timeframe
    if download_date:
        date.fromisoformat(download_date)
        folders = [base / download_date]
    else:
        folders = []
        for folder in base.iterdir() if base.exists() else []:
            try:
                date.fromisoformat(folder.name)
            except ValueError:
                continue
            if folder.is_dir():
                folders.append(folder)
        folders.sort(reverse=True)
    folder = next((f for f in folders if all((f / symbol_filename(s)).is_file() for s in symbols)), None)
    if folder is None:
        raise ValueError(f"No complete {timeframe} bar batch for {len(symbols)} symbols under {base}; download the missing histories or select --download-date")
    result = {"schema_version": 1, "series": {}, "notices": [], "bar_files": [],
              "symbol_fetched_at": {}, "session_timezones": {}, "download_date": folder.name}
    for symbol in symbols:
        path = folder / symbol_filename(symbol)
        content = path.read_bytes()
        payload = json.loads(content)
        if payload.get("timeframe") != timeframe or set(payload["series"]) != {symbol}:
            raise ValueError(f"Unexpected symbol/timeframe in {path.name}")
        if result.get("provider", payload["provider"]) != payload["provider"]:
            raise ValueError("Cannot mix bar providers within a batch")
        result["provider"] = payload["provider"]
        result["series"][symbol] = payload["series"][symbol]
        result["symbol_fetched_at"][symbol] = payload["fetched_at"]
        result["session_timezones"].update(payload.get("session_timezones", {}))
        result["notices"] = sorted(set(result["notices"]) | set(payload.get("notices", [])))
        result["bar_files"].append({"symbol": symbol, "file": str(path.relative_to(root)),
                                    "sha256": hashlib.sha256(content).hexdigest()})
    result["fetched_at"] = min(result["symbol_fetched_at"].values(), key=lambda x: datetime.fromisoformat(x.replace("Z", "+00:00")))
    return result
