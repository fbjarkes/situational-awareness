"""Reproduce the breadth threshold event study from local TradingView downloads."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from statistics import mean, median
from bar_store import ROOT as DATA_ROOT, load_bars

ROOT = Path(__file__).resolve().parent
HORIZONS = (10, 20, 30, 50, 100, 200)
THRESHOLDS = (30, 25, 20)


def load_prices(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    prices = {}
    if "series" in payload:
        bars = next(iter(payload["series"].values()))
        for bar in bars:
            day = datetime.fromtimestamp(bar["t"], timezone.utc).date().isoformat()
            if bar["c"] is not None:
                prices[day] = float(bar["c"])
        return prices
    for page in payload["pages"]:
        if not page.get("success"):
            raise ValueError(f"Unsuccessful data page in {path}")
        bars = page["bars"]
        for timestamp, close in zip(bars["t"], bars["c"], strict=True):
            if close is not None:
                day = datetime.fromtimestamp(timestamp, timezone.utc).date().isoformat()
                prices[day] = float(close)
    return prices


def crossings(prices, threshold):
    days = sorted(prices)
    return [day for previous, day in zip(days, days[1:])
            if prices[previous] >= threshold and prices[day] < threshold]


def study(spy, indicators):
    days = sorted(spy)
    positions = {day: i for i, day in enumerate(days)}
    events, summary = [], []
    for indicator, prices in indicators.items():
        eligible = sorted(set(prices) & set(spy))
        if not eligible:
            raise ValueError(f"No common dates for {indicator}")
        for threshold in THRESHOLDS:
            signals = crossings(prices, threshold)
            for horizon in HORIZONS:
                samples = []
                for signal in signals:
                    if signal not in positions:
                        continue
                    i = positions[signal]
                    if i + horizon >= len(days):
                        continue
                    exit_day = days[i + horizon]
                    value = (spy[exit_day] / spy[signal] - 1) * 100
                    samples.append((i, value))
                    events.append({"indicator": indicator, "threshold": threshold,
                                   "signal_date": signal, "horizon": horizon,
                                   "exit_date": exit_day, "entry_close": spy[signal],
                                   "exit_close": spy[exit_day], "return_pct": value,
                                   "breadth_close": prices[signal]})
                baseline = [(spy[days[positions[d] + horizon]] / spy[d] - 1) * 100
                            for d in eligible if positions[d] + horizon < len(days)]
                values = [v for _, v in samples]
                summary.append({"indicator": indicator, "threshold": threshold,
                                "horizon": horizon, "crossings": len(signals),
                                "missing_spy_dates": sum(d not in positions for d in signals),
                                "n": len(values),
                                "immature": sum(d in positions and positions[d] + horizon >= len(days) for d in signals),
                                "mean_pct": mean(values) if values else None,
                                "median_pct": median(values) if values else None,
                                "win_rate_pct": 100 * mean(v > 0 for v in values) if values else None,
                                "worst_pct": min(values) if values else None,
                                "best_pct": max(values) if values else None,
                                "baseline_n": len(baseline),
                                "baseline_mean_pct": mean(baseline) if baseline else None,
                                "baseline_win_rate_pct": 100 * mean(v > 0 for v in baseline) if baseline else None,
                                "overlapping_windows": sum(b[0] < a[0] + horizon for a, b in zip(samples, samples[1:])),
                                "start": eligible[0], "end": eligible[-1]})
    return events, summary


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(summary):
    lines = ["# Breadth threshold event study", "",
             f"Shared observation period: {summary[0]['start']} to {summary[0]['end']}.", "",
             "SPY forward price returns, in percent. Horizons count SPY trading sessions.", "",
             "Crossing: previous available indicator close >= threshold and current close < threshold.",
             "Each indicator is tested separately; this does not test both-below or either-below combinations.",
             "Entry is the signal-session SPY close; no next-session execution or transaction costs are modeled.",
             "Prices are split-adjusted, not dividend-adjusted. This is a descriptive event study, not an executable strategy backtest.", "",
             "Each cell below is mean return / median return / positive-return frequency (N mature events).", ""]
    for indicator in dict.fromkeys(s["indicator"] for s in summary):
        lines += [f"## {indicator}", "", "| Threshold | " + " | ".join(f"{h} days" for h in HORIZONS) + " |",
                  "|---|" + "---|" * len(HORIZONS)]
        for threshold in THRESHOLDS:
            rows = [s for s in summary if s["indicator"] == indicator and s["threshold"] == threshold]
            cells = [f"{r['mean_pct']:.2f}% / {r['median_pct']:.2f}% / {r['win_rate_pct']:.0f}% (N={r['n']})" if r['n'] else "Unavailable" for r in rows]
            lines.append(f"| Below {threshold} | " + " | ".join(cells) + " |")
        baseline = [s for s in summary if s["indicator"] == indicator and s["threshold"] == 30]
        lines += ["| Unconditional mean | " + " | ".join(f"{r['baseline_mean_pct']:.2f}%" for r in baseline) + " |", ""]
    lines += ["## Limitations", "",
              "- Recent signals without a complete forward horizon are excluded separately for each horizon; counts therefore differ.",
              "- Crossings use adjacent available indicator observations; missing sessions are not reconstructed.",
              "- Every recrossing counts. Return windows can overlap and events cluster within market declines; samples are not independent.",
              "- The unconditional baseline uses all available common starting dates, with the same maturity requirement per horizon.",
              "- The baseline is descriptive, without regime matching, significance testing, or multiple-testing correction.",
              "- Worst/best returns in CSV are terminal horizon returns, not maximum interim drawdowns.",
              "- Provider history may contain revisions or constituent changes. Input hashes identify the downloaded snapshot.",
              "- Neither threshold rarity nor a robust buying rule is established by this simple study.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DATA_ROOT, help="Raw bar store root")
    parser.add_argument("--download-date", help="Select a dated batch; default latest containing all study symbols")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/breadth-study")
    args = parser.parse_args()
    payload = load_bars(["AMEX:SPY", "INDEX:MMOH", "INDEX:MMOF"], args.data, download_date=args.download_date)
    paths = {item["symbol"]: args.data / item["file"] for item in payload["bar_files"]}
    spy = load_prices(paths["AMEX:SPY"])
    indicators = {s: load_prices(paths[f"INDEX:{s}"]) for s in ("MMOH", "MMOF")}
    events, summary = study(spy, indicators)
    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "events.csv", events)
    write_csv(args.output / "summary.csv", summary)
    (args.output / "study.md").write_text(render_markdown(summary), encoding="utf-8")
    metadata = {"provider": "tradingview", "generated_at": datetime.now(timezone.utc).isoformat(),
                "inputs": {s: {"file": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                                  "fetched_at": json.loads(p.read_text())["fetched_at"]} for s, p in paths.items()}}
    (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(render_markdown(summary))


if __name__ == "__main__":
    main()
