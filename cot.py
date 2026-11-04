"""CFTC consolidated futures-only history and optional TradingView price context.

Download/update: uv run cot.py --refresh
"""
import argparse
import csv
from datetime import date, datetime, timedelta, timezone
import hashlib
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen
import zipfile
from zoneinfo import ZoneInfo

from bar_store import load_bars, ROOT as BAR_ROOT

ROOT = Path(__file__).resolve().parent / "data/cot"
MARKETS = {"13874+": ("S&P 500", "CME_MINI:ES1!"), "20974+": ("Nasdaq-100", "CME_MINI:NQ1!")}
GROUPS = {"dealers": ("Dealers", "Dealer", "#ff7676"),
          "asset_managers": ("Asset managers", "Asset_Mgr", "#67ddc4"),
          "leveraged_funds": ("Leveraged funds", "Lev_Money", "#a898ff"),
          "other_reportables": ("Other reportables", "Other_Rept", "#ffc078"),
          "nonreportable": ("Non-reportable", "NonRept", "#80bfff")}


def parse_history(rows):
    markets = {code: {} for code in MARKETS}
    for row in rows:
        code = row["CFTC_Contract_Market_Code"].strip()
        if code not in MARKETS:
            continue
        observed = date.fromisoformat(row["Report_Date_as_YYYY-MM-DD"].strip()).isoformat()
        groups = {}
        for key, (_, prefix, _) in GROUPS.items():
            long = int(row[f"{prefix}_Positions_Long_All"].replace(',', ''))
            short = int(row[f"{prefix}_Positions_Short_All"].replace(',', ''))
            if min(long, short) < 0:
                raise ValueError("COT gross positions must be nonnegative")
            groups[key] = {"long": long, "short": short, "net": long - short}
        residual = sum(g["net"] for g in groups.values())
        if abs(residual) > 5:
            raise ValueError("COT categories do not reconcile to zero")
        point = {"date": observed, "open_interest": int(row["Open_Interest_All"].replace(',', '')),
                 "net_reconciliation_residual": residual, "groups": groups}
        if observed in markets[code] and markets[code][observed] != point:
            raise ValueError(f"Conflicting COT rows for {code} on {observed}")
        markets[code][observed] = point
    return {code: sorted(points.values(), key=lambda p: p["date"]) for code, points in markets.items()}


def download_history(*, root=ROOT, refresh=False, now=None):
    now = now or datetime.now(timezone.utc)
    current = now.astimezone(ZoneInfo("Europe/Stockholm")).date()
    folder = root / current.isoformat()
    folder.mkdir(parents=True, exist_ok=True)
    sources, rows = [], []
    for year in (current.year - 1, current.year):
        path = folder / f"fut_fin_txt_{year}.zip"
        meta_path = folder / f"fut_fin_txt_{year}.metadata.json"
        if refresh or not path.exists() or not meta_path.exists():
            url = f"https://www.cftc.gov/files/dea/history/fut_fin_txt_{year}.zip"
            raw = urlopen(Request(url, headers={"User-Agent": "situational-awareness/1.0"}), timeout=40).read()
            fetched = datetime.now(timezone.utc).isoformat()
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                member = next(n for n in archive.namelist() if n.lower().endswith('.txt'))
            path.write_bytes(raw)
            meta_path.write_text(json.dumps({"provider": "CFTC", "source_url": url, "fetched_at": fetched,
                                             "sha256": hashlib.sha256(raw).hexdigest(), "member": member}, indent=2), encoding="utf-8")
        raw = path.read_bytes()
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        if hashlib.sha256(raw).hexdigest() != metadata["sha256"]:
            raise ValueError(f"Archive hash mismatch: {path.name}")
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            rows.extend(csv.DictReader(io.StringIO(archive.read(metadata["member"]).decode('utf-8-sig'))))
        sources.append({**metadata, "file": str(path)})
    payload = {"provider": "CFTC", "report": "TFF consolidated futures only", "sources": sources,
               "generated_at": datetime.now(timezone.utc).isoformat(), "markets": parse_history(rows)}
    if any(not points for points in payload["markets"].values()):
        raise ValueError("Missing consolidated index history")
    path = root / "sp500-nasdaq-history.json"
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False) + '\n', encoding="utf-8")
    temporary.replace(path)
    return payload


def futures_session_date(timestamp):
    opened = datetime.fromtimestamp(timestamp, timezone.utc).astimezone(ZoneInfo("America/Chicago"))
    return opened.date() + (timedelta(days=1) if opened.hour >= 17 else timedelta())


def build_cot_section(as_of, *, root=ROOT, bar_root=BAR_ROOT, months=12):
    result = {"provider": "CFTC", "markets": [], "used_symbols": [], "months": months}
    path = root / "sp500-nasdaq-history.json"
    if not path.exists():
        result["unavailable"] = "COT history unavailable; run uv run cot.py --refresh."
        return result
    raw = path.read_bytes()
    payload = json.loads(raw)
    result.update(input_file=str(path), input_sha256=hashlib.sha256(raw).hexdigest(), sources=payload["sources"])
    start = as_of - timedelta(days=round(months * 365.25 / 12))
    try:
        prices = load_bars([market[1] for market in MARKETS.values()], bar_root, provider="tradingview")
        result["price_inputs"] = prices["bar_files"]
        result["price_download_date"] = prices["download_date"]
    except ValueError:
        prices = {"series": {}}
    for code, (title, symbol) in MARKETS.items():
        # Weekly positions are plotted on their observation dates, not publication
        # dates. This descriptive chart is not a point-in-time trading backtest.
        points = [p for p in payload["markets"].get(code, []) if start.isoformat() <= p["date"] <= as_of.isoformat()]
        if not points:
            continue
        latest = points[-1]
        previous = points[-2] if len(points) > 1 else None
        market = {"code": code, "title": title, "symbol": symbol, "points": points,
                  "as_of": latest["date"], "prices": [], "start": start.isoformat(), "end": as_of.isoformat()}
        for bar in prices["series"].get(symbol, []):
            session = futures_session_date(bar["t"])
            if start <= session <= as_of and all(bar.get(k) is not None for k in ('o', 'h', 'l', 'c')):
                market["prices"].append({"date": session.isoformat(), **{k: bar[k] for k in ('o', 'h', 'l', 'c')}})
        if market["prices"]:
            result["used_symbols"].append(symbol)
            fetched = prices.get("symbol_fetched_at", {}).get(symbol, prices.get("fetched_at"))
            if fetched:
                fetched_local = datetime.fromisoformat(fetched.replace('Z', '+00:00')).astimezone(ZoneInfo('America/Chicago'))
                market["price_intraday"] = (market["prices"][-1]["date"] == fetched_local.date().isoformat()
                                            and fetched_local.hour < 16)
        fund = latest["groups"]["leveraged_funds"]["net"]
        manager = latest["groups"]["asset_managers"]["net"]
        change = fund - previous["groups"]["leveraged_funds"]["net"] if previous else None
        market["interpretation"] = (f'Asset managers are net {"long" if manager >= 0 else "short"} {abs(manager):,} contracts; leveraged funds are net {"long" if fund >= 0 else "short"} {abs(fund):,}'
                                    + (f', a {change:+,} change from the previous observation. ' if change is not None else '. ')
                                    + 'These are portfolio positions that can include hedging; this chart does not establish a positioning extreme or a reversal signal.')
        result["markets"].append(market)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    history = download_history(refresh=args.refresh)
    for code, points in history['markets'].items():
        print(MARKETS[code][0], len(points), 'weekly observations through', points[-1]['date'])
