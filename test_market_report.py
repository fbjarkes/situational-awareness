import importlib.util
import json
from datetime import date, datetime, timezone
from pathlib import Path
import tempfile
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location("market_report", Path(__file__).with_name("market-report.py"))
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


def spy_bars(n=260, end=date(2026, 10, 23)):
    """Rising closes with a three-session decline at the end."""
    from datetime import timedelta
    closes = [100 + i for i in range(n - 3)] + [n + 95, n + 94, n + 93]
    return [{"t": int(datetime.combine(end - timedelta(days=n - 1 - i), datetime.min.time(), timezone.utc).timestamp()) + 4 * 3600,
             "c": float(c)} for i, c in enumerate(closes)]


def fake_alpaca(symbols, start, end, *, feed, **_):
    return {"schema_version": 1, "provider": "alpaca", "fetched_at": "2026-10-24T00:00:00Z", "feed": feed,
            "adjustment": "split", "session_timezones": {"SPY": "America/New_York"},
            "series": {"SPY": spy_bars()}, "empty_symbols": []}


class ReportTests(unittest.TestCase):
    def payload(self):
        bars = [{"t": int(datetime(2026, 10, day, 13, 30, tzinfo=timezone.utc).timestamp()),
                 "c": float(day)} for day in (15, 16, 19, 20, 21, 22, 23, 24)]
        return {"provider": "tradingview", "fetched_at": "2026-10-24T00:00:00Z",
                "series": {symbol: bars for symbol in report.SYMBOLS}}

    def ny(self, day, hour=10):
        return datetime(2026, 10, day, hour, 0, tzinfo=report.NY)

    def test_historical_filter_and_changes(self):
        result = report.build_report(self.payload(), date(2026, 10, 23), 6, "test", self.ny(24))
        series = result["series"]["INDEX:MMOH"]
        self.assertEqual(series["latest"], {"date": "2026-10-23", "close": 23.0})
        self.assertEqual(series["daily_change"], 1)
        self.assertEqual(series["five_session_change"], 7)
        self.assertTrue(all(b["date"] <= "2026-10-23" for b in series["observations"]))

    def test_current_day_is_intraday(self):
        payload = self.payload()
        payload["fetched_at"] = "2026-10-24T19:00:00Z"  # 15:00 ET
        result = report.build_report(payload, date(2026, 10, 24), 6, "test", self.ny(24, 15))
        series = result["series"]["INDEX:MMOF"]
        self.assertEqual(series["latest"]["date"], "2026-10-24")
        self.assertEqual(series["latest_status"], "intraday")
        self.assertEqual(series["as_of"], "intraday 2026-10-24 15:00 ET")
        self.assertTrue(any("intraday" in n for n in result["notes"]))

    def test_close_only_excludes_current_day(self):
        result = report.build_report(self.payload(), date(2026, 10, 24), 6, "test", self.ny(24), close_only=True)
        self.assertEqual(result["series"]["INDEX:MMOF"]["latest"]["date"], "2026-10-23")

    def test_mixed_dates_are_stated(self):
        payload = self.payload()
        payload["fetched_at"] = "2026-10-24T19:00:00Z"
        payload["series"]["INDEX:MMOF"] = payload["series"]["INDEX:MMOF"][:-1]
        result = report.build_report(payload, date(2026, 10, 24), 6, "test", self.ny(24, 15))
        self.assertEqual(result["series"]["INDEX:MMOF"]["as_of"], "close 2026-10-23")
        self.assertTrue(any("MMOF: using the 2026-10-23 close" in n for n in result["notes"]))
        self.assertTrue(any("different dates" in n for n in result["notes"]))
        html = report.render_html(result)
        self.assertIn("(close 2026-10-23)", html)
        self.assertIn("(intraday 2026-10-24 15:00 ET)", html)

    def test_missing_and_stale_observations(self):
        with self.assertRaisesRegex(ValueError, "No observations"):
            report.build_report(self.payload(), date(2026, 1, 1), 1, "test", self.ny(24))
        result = report.build_report(self.payload(), date(2026, 11, 1), 1, "test",
                                     datetime(2026, 11, 2, 10, tzinfo=report.NY))
        self.assertTrue(any("8 calendar days" in w for w in result["warnings"]))

    def test_month_end(self):
        self.assertEqual(report.months_before(date(2024, 3, 31), 1), date(2024, 2, 29))

    def test_vix_low_metric_and_historical_cutoff(self):
        payload = self.payload()
        bars = payload["series"]["INDEX:MMOH"]
        payload["series"] = {"CBOE:VIX": [{**bar, "c": 100 - bar["c"]} for bar in bars]}
        result = report.vix_section(payload, date(2026, 10, 23), 6, self.ny(24), period=365)
        self.assertEqual(result["latest"]["date"], "2026-10-23")
        self.assertEqual(result["metrics"]["day_low"], 7)
        self.assertTrue(result["day_low_lower_bound"])
        payload["fetched_at"] = "2026-10-24T20:05:00Z"
        current = report.vix_section(payload, date(2026, 10, 24), 6, self.ny(24, 16))
        self.assertEqual(current["latest_status"], "intraday")
        self.assertIn("provisional", current["interpretation"])

    def test_design_navigation_and_percentage_axes(self):
        from html.parser import HTMLParser

        class Anchors(HTMLParser):
            def __init__(self):
                super().__init__()
                self.ids = []
                self.targets = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if "id" in attrs:
                    self.ids.append(attrs["id"])
                if tag == "a" and attrs.get("href", "").startswith("#"):
                    self.targets.append(attrs["href"][1:])

        result = report.build_report(self.payload(), date(2026, 10, 23), 6, "test", self.ny(24))
        result["notes"].append("Using the latest available closing observations.")
        html = report.render_html(result)
        anchors = Anchors()
        anchors.feed(html)
        self.assertEqual(len(anchors.ids), len(set(anchors.ids)))
        self.assertTrue(set(anchors.targets) <= set(anchors.ids))
        self.assertIn('aria-label="Report sections"', html)
        self.assertIn('<details class="data-status">', html)
        svg = report.chart_svg(result)
        self.assertIn('>100%</text>', svg)
        self.assertIn('>0%</text>', svg)
        self.assertIn('stroke-dasharray', svg)
        self.assertIn('viewBox="0 0 520 350"', report.chart_svg(result, compact=True))

    def test_gdx_section_respects_date_and_retains_coverage(self):
        from breadth import calculate_breadth
        result = report.build_report(self.payload(), date(2026, 10, 23), 6, "test", self.ny(24))
        prices = {"a": {f"2026-10-{d:02}": float(d) for d in (19, 20, 21, 22, 23, 24)},
                  "b": {f"2026-10-{d:02}": 50.0 - d for d in (19, 20, 21, 22, 23, 24)}}
        payload = calculate_breadth(["a", "b"], prices, 2, name="CUSTOM:GDX-SMA2", universe_as_of="2026-10-22")
        with tempfile.TemporaryDirectory(dir=report.ROOT / "reports") as folder:
            path = Path(folder) / "gdx.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            report.attach_gdx_breadth(result, path, self.ny(24), False)
        section = result["gdx_breadth"]
        latest = next(iter(section["series"].values()))["latest"]
        self.assertEqual(latest["date"], "2026-10-23")
        self.assertEqual(latest["close"], 50)
        self.assertEqual(section["coverage"]["eligible"], 2)
        html = report.render_html(result)
        self.assertIn("GDX breadth", html)
        self.assertIn("Coverage 2/2", html)

    def test_knowledge_distinguishes_level_from_crossing(self):
        result = report.build_report(self.payload(), date(2026, 10, 23), 6, "test", self.ny(24))
        report.attach_breadth_knowledge(result)
        self.assertIn("Neither index made a new downward crossing", result["interpretation"])
        self.assertIn("100-day average", result["interpretation"])
        for series in result["series"].values():
            series["latest"]["close"] = 19
            series["daily_change"] = -2
        text = report.breadth_interpretation(result)
        self.assertIn("New downward crossings: MMOH below 20, MMOF below 20", text)
        self.assertIn("does not establish a buying signal", text)

    def test_cli_generates_both_artifacts(self):
        (report.ROOT / "reports").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=report.ROOT / "reports") as folder:
            snapshot = Path(folder) / "fixture.json"
            snapshot.write_text(json.dumps(self.payload()), encoding="utf-8")
            result = report.main(["--date", "2026-10-23", "--snapshot", str(snapshot), "--output", folder])
            self.assertEqual(result, 0)
            data = json.loads((Path(folder) / "market-report-2026-10-23.json").read_text())
            self.assertEqual(data["series"]["INDEX:MMOH"]["latest"]["close"], 23.0)
            html = (Path(folder) / "market-report-2026-10-23.html").read_text(encoding="utf-8")
            self.assertIn("<svg", html)
            self.assertIn("MMOF", html)

    def test_alpaca_labels_tradingview_only_breadth(self):
        from bar_store import save_bars
        (report.ROOT / "reports").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=report.ROOT / "reports") as folder:
            root = Path(folder) / "store"
            save_bars(self.payload(), root)
            missing = Path(folder) / "no-gdx.json"
            with mock.patch.object(report, "fetch_alpaca_daily", fake_alpaca):
                self.assertEqual(report.main(["--date", "2026-10-23", "--provider", "alpaca", "--data-root", str(root),
                                              "--gdx-breadth", str(missing), "--output", folder]), 0)
            data = json.loads((Path(folder) / "market-report-2026-10-23.json").read_text())
            self.assertEqual(data["requested_provider"], "alpaca")
            self.assertEqual({c["status"] for c in data["provider_coverage"] if c["section"] == "Market breadth"}, {"substituted"})
            self.assertTrue(any(c["symbol"] == "CBOE:VIX" and c["status"] == "unavailable" for c in data["provider_coverage"]))
            self.assertEqual(data["provider"], "tradingview")
            html = (Path(folder) / "market-report-2026-10-23.html").read_text(encoding="utf-8")
            self.assertIn("Provider limitations · 3", html)
            self.assertIn("not available from Alpaca", html)
            self.assertIn('class="source-note"', html)
            self.assertEqual(data["spy"]["provider"], "alpaca")
            self.assertEqual(data["spy"]["metrics"]["cons_down_days"], 3)
            self.assertEqual(data["run_status"]["downloaded_symbols"], 1)
            self.assertIn("Alpaca · iex feed · SPY", html)

    def test_alpaca_without_stored_breadth_renders_unavailable(self):
        (report.ROOT / "reports").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=report.ROOT / "reports") as folder:
            with mock.patch.object(report, "fetch_alpaca_daily", fake_alpaca):
                self.assertEqual(report.main(["--date", "2026-10-23", "--provider", "alpaca", "--data-root", str(Path(folder) / "empty"),
                                              "--gdx-breadth", str(Path(folder) / "no-gdx.json"), "--output", folder]), 0)
            html = (Path(folder) / "market-report-2026-10-23.html").read_text(encoding="utf-8")
            self.assertIn("No breadth data for this provider", html)
            self.assertIn("Unavailable from the selected provider", html)
            data = json.loads((Path(folder) / "market-report-2026-10-23.json").read_text())
            self.assertEqual(data["series"], {})
            self.assertEqual({c["status"] for c in data["provider_coverage"]}, {"unavailable"})

    def test_gdx_alpaca_snapshot_shows_unavailable_constituents(self):
        from breadth import calculate_breadth
        result = report.build_report(self.payload(), date(2026, 10, 23), 6, "test", self.ny(24))
        prices = {"NYSE:NEM": {f"2026-10-{d:02}": float(d) for d in (19, 20, 21, 22, 23)}}
        payload = calculate_breadth(["NYSE:NEM", "TSX:LUG"], prices, 2, name="CUSTOM:GDX-SMA2")
        payload["input_provider"] = "alpaca"
        payload["universe"]["provider_unavailable"] = {"TSX:LUG": "Not a US listing."}
        with tempfile.TemporaryDirectory(dir=report.ROOT / "reports") as folder:
            path = Path(folder) / "gdx.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            report.attach_gdx_breadth(result, path, self.ny(24), False)
        self.assertEqual(result["provider_coverage"][0]["status"], "partial")
        html = report.render_html(result)
        self.assertIn("1 of 2 GDX constituents", html)
        self.assertIn("Constituent prices: Alpaca.", html)

    def test_spy_card_from_stored_tradingview_bars(self):
        from bar_store import save_bars
        (report.ROOT / "reports").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=report.ROOT / "reports") as folder:
            root = Path(folder) / "store"
            save_bars(self.payload(), root)
            save_bars({"provider": "tradingview", "fetched_at": "2026-10-24T00:00:00Z", "series": {"AMEX:SPY": spy_bars()}}, root)
            self.assertEqual(report.main(["--date", "2026-10-23", "--data-root", str(root),
                                          "--gdx-breadth", str(Path(folder) / "none.json"), "--output", folder]), 0)
            data = json.loads((Path(folder) / "market-report-2026-10-23.json").read_text())
            m = data["spy"]["metrics"]
            self.assertEqual(m["close"], 353.0)
            self.assertEqual(m["cons_down_days"], 3)
            # A steady rise stays above its 50-day SMA for all 211 evaluable sessions.
            self.assertEqual(m["cons_days_above_sma50"], 211)
            self.assertTrue(m["lower_bound"]["cons_days_above_sma50"])
            closes = [100 + i for i in range(257)] + [355, 354, 353]
            self.assertAlmostEqual(m["distance_from_sma200_pct"], 100 * (353 / (sum(closes[-200:]) / 200) - 1))
            self.assertFalse(m["lower_bound"]["cons_down_days"])
            html = (Path(folder) / "market-report-2026-10-23.html").read_text(encoding="utf-8")
            self.assertIn("Cons. down days", html)
            self.assertIn("Distance from 200-day SMA", html)
            self.assertIn("SPY 353.00", html)
            self.assertIn("≥211", html)

    def test_spy_unavailable_without_stored_history(self):
        result = report.build_report(self.payload(), date(2026, 10, 23), 6, "test", self.ny(24))
        result["spy"] = report.spy_section(None, "tradingview", date(2026, 10, 23), 6, self.ny(24), False, "unavailable")
        html = report.render_html(result)
        self.assertIn("No SPY data", html)
        self.assertIn("SPY data unavailable", html)

    def test_knowledge_records_alpaca_unavailability(self):
        for symbol in report.SYMBOLS:
            self.assertEqual(report.provider_availability(symbol, "alpaca")["status"], "unavailable")
            self.assertEqual(report.provider_availability(symbol, "tradingview")["symbol"], symbol)


if __name__ == "__main__":
    unittest.main()
