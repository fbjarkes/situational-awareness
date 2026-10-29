from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest

from bar_store import save_bars
from theme_returns import basket_returns, build_theme_returns, prices_from_payload, theme_universes
from report_design import theme_returns_card


class ThemeReturnTests(unittest.TestCase):
    def test_daily_rebalancing_not_buy_and_hold_average(self):
        days = [date(2026, 10, 19) + timedelta(days=i) for i in range(6)]
        prices = {"A": dict(zip(days, [100, 200, 100, 100, 100, 100])),
                  "B": dict(zip(days, [100, 50, 100, 100, 100, 100]))}
        result, _, _ = basket_returns(prices, days, days[-1])
        self.assertAlmostEqual(result["1W"], 56.25)

    def test_missing_session_does_not_silently_drop_stock(self):
        days = [date(2026, 10, 19) + timedelta(days=i) for i in range(6)]
        prices = {"A": {d: 100 for d in days}, "B": {d: 100 for d in days}}
        del prices["B"][days[2]]
        result, _, reasons = basket_returns(prices, days, days[-1])
        self.assertIsNone(result["1W"])
        self.assertIn("Incomplete", reasons["1W"])

    def test_calendar_month_and_insufficient_ipo_history(self):
        days = [date(2026, 9, 1) + timedelta(days=i) for i in range(60)]
        days = [d for d in days if d.weekday() < 5]
        prices = {"A": {d: 100 + i for i, d in enumerate(days)}}
        result, starts, _ = basket_returns(prices, days, date(2026, 10, 30))
        self.assertEqual(starts["1M"], "2026-09-30")
        self.assertIsNotNone(result["1M"])
        self.assertIsNone(result["3M"])
        del prices["A"][date(2026, 9, 30)]
        self.assertIsNone(basket_returns(prices, days, days[-1])[0]["1M"])

    def test_reused_ticker_and_future_cutoff(self):
        def bar(day):
            return {"t": int(datetime.fromisoformat(day + "T14:00:00+00:00").timestamp()), "c": 100}
        payload = {"series": {"NASDAQ:SPCX": [bar(d) for d in ("2026-06-11", "2026-06-12", "2026-06-15")]}}
        prices = prices_from_payload(payload, ["NASDAQ:SPCX"], date(2026, 6, 12))
        self.assertEqual(list(prices["NASDAQ:SPCX"]), [date(2026, 6, 12)])

    def test_registry_deduplication_and_fund_exclusion(self):
        root = Path(__file__).parent / "knowledge"
        themes = theme_universes(root, Path(__file__).parent / "data/gdx-symbol-map.json")
        crypto = next(t for t in themes if t["id"] == "crypto-blockchain")
        self.assertNotIn("AMEX:BITO", crypto["symbols"])
        self.assertNotIn("NASDAQ:HOOD", crypto["symbols"])
        mobility = next(t for t in themes if t["id"] == "mobility")
        self.assertEqual(mobility["symbols"].count("NYSE:JOBY"), 1)

    def test_pinned_batch_provider_and_html(self):
        Path("reports").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir="reports") as folder:
            root = Path(folder)
            knowledge = root / "knowledge"
            (knowledge / "themes").mkdir(parents=True)
            (knowledge / "themes/themes.md").write_text('---\nthemes:\n  - id: demo\n    title: Demo <theme>\n---\n', encoding="utf-8")
            (knowledge / "themes/theme-memberships.md").write_text('# Memberships\n| NASDAQ:A | demo | | core universe | core | | | | | |\n', encoding="utf-8")
            bars = [{"t": int(datetime(2026, 10, d, 14, tzinfo=timezone.utc).timestamp()), "c": 100 + d} for d in range(19, 25)]
            save_bars({"provider": "tradingview", "fetched_at": "2026-10-25T10:00:00Z", "adjustment": "split",
                       "series": {"NASDAQ:A": bars, "AMEX:SPY": bars}}, root)
            result = build_theme_returns(knowledge, date(2026, 10, 24), data_root=root, download_date="2026-10-25")
            self.assertIsNotNone(result["rows"][0]["returns"]["1W"])
            self.assertEqual(len(result["input_bar_files"]), 2)
            html = theme_returns_card(result)
            self.assertIn("Demo &lt;theme&gt;", html)
            self.assertIn("12M", html)
            self.assertIn("N/A", html)
            missing = build_theme_returns(knowledge, date(2026, 10, 24), data_root=root, download_date="2026-10-26")
            self.assertIsNone(missing["rows"][0]["returns"]["1W"])


if __name__ == "__main__":
    unittest.main()
