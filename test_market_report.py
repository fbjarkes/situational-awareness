import importlib.util
import json
from datetime import date, datetime, timezone
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("market_report", Path(__file__).with_name("market-report.py"))
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


class ReportTests(unittest.TestCase):
    def payload(self):
        bars = [{"t": int(datetime(2026, 10, day, 13, 30, tzinfo=timezone.utc).timestamp()),
                 "c": float(day)} for day in (15, 16, 19, 20, 21, 22, 23, 24)]
        return {"provider": "tradingview", "fetched_at": "2026-10-24T00:00:00Z",
                "series": {symbol: bars for symbol in report.SYMBOLS}}

    def test_historical_filter_and_changes(self):
        result = report.build_report(self.payload(), date(2026, 10, 23), 6, "test", date(2026, 10, 24))
        series = result["series"]["INDEX:MMOH"]
        self.assertEqual(series["latest"], {"date": "2026-10-23", "close": 23.0})
        self.assertEqual(series["daily_change"], 1)
        self.assertEqual(series["five_session_change"], 7)
        self.assertTrue(all(b["date"] <= "2026-10-23" for b in series["observations"]))

    def test_current_day_is_excluded(self):
        result = report.build_report(self.payload(), date(2026, 10, 24), 6, "test", date(2026, 10, 24))
        self.assertEqual(result["series"]["INDEX:MMOF"]["latest"]["date"], "2026-10-23")

    def test_missing_and_stale_observations(self):
        with self.assertRaisesRegex(ValueError, "No observations"):
            report.build_report(self.payload(), date(2026, 1, 1), 1, "test", date(2026, 10, 24))
        result = report.build_report(self.payload(), date(2026, 11, 1), 1, "test", date(2026, 11, 2))
        self.assertTrue(any("8 calendar days" in w for w in result["warnings"]))

    def test_month_end(self):
        self.assertEqual(report.months_before(date(2024, 3, 31), 1), date(2024, 2, 29))

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


if __name__ == "__main__":
    unittest.main()
