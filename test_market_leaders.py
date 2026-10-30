import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest

from bar_store import save_bars
from market_leaders import build_market_leaders, weighted_rs, closing_high_distance
from report_design import market_leaders_card


class MarketLeaderTests(unittest.TestCase):
    def test_high_proximity_full_window_and_penalty(self):
        days = [date(2025, 1, 1) + timedelta(days=i) for i in range(253)]
        prices = {d: 100.0 for d in days}
        prices[days[0]] = 1000  # Excluded from the trailing 252-session window.
        prices[days[-1]] = 80
        high = closing_high_distance(prices, days)
        self.assertAlmostEqual(high['distance_pct'], -20)
        self.assertEqual(high['high_close'], 100)
        self.assertAlmostEqual(weighted_rs({'rs': 10, 'high': -20}, {'rs': .8, 'high': .2}), 4)
        self.assertIsNone(closing_high_distance(prices, days[-251:]))
        del prices[days[-3]]
        self.assertIsNone(closing_high_distance(prices, days))

    def test_weighted_rs_and_missing_horizon(self):
        self.assertAlmostEqual(weighted_rs({"a": 10, "b": 30}, {"a": 1, "b": 3}), 25)
        self.assertIsNone(weighted_rs({"a": 10, "b": None}, {"a": 1, "b": 1}))
        with self.assertRaises(ValueError):
            weighted_rs({"a": 10}, {"a": -1})

    def test_deduplicated_ranking_extended_missing_and_top_ten(self):
        with tempfile.TemporaryDirectory(dir="reports") as directory:
            root = Path(directory)
            knowledge = root / "knowledge"
            (knowledge / "themes").mkdir(parents=True)
            (knowledge / "themes/themes.md").write_text('---\nthemes:\n  - id: demo\n    title: Demo\n---\n', encoding="utf-8")
            (knowledge / "market-leaders.md").write_text('---\nmarket_report:\n  weights: {1W: 0.20, 1M: 0.20, 3M: 0.20, 6M: 0.20}\n  proximity_weight: 0.20\n---\n', encoding="utf-8")
            table = '# Memberships\n'
            symbols = [f'NASDAQ:S{i:02}' for i in range(12)]
            for symbol in symbols:
                table += f'| {symbol} | demo | | core universe | core | | | | | |\n'
            table += '| NASDAQ:S11 | demo | | extended candidate | core | | | | | |\n'
            table += '| NASDAQ:MISSING | demo | | extended candidate | core | | | | | |\n'
            (knowledge / "themes/theme-memberships.md").write_text(table, encoding="utf-8")
            days = [date(2025, 11, 1) + timedelta(days=i) for i in range(364)]
            days = [d for d in days if d.weekday() < 5]
            def bars(rate):
                return [{"t": int(datetime(d.year, d.month, d.day, 14, tzinfo=timezone.utc).timestamp()),
                         "c": 100 * rate ** i} for i, d in enumerate(days)]
            series = {s: bars(1 + (i + 1) / 1000) for i, s in enumerate(symbols)}
            series['AMEX:SPY'] = bars(1)
            save_bars({"provider": "tradingview", "fetched_at": "2026-10-30T20:00:00Z", "adjustment": "split", "series": series}, root)
            result = build_market_leaders(knowledge, days[-1], download_date="2026-10-30", data_root=root)
            self.assertEqual(result['universe_size'], 13)
            self.assertEqual(result['eligible'], 12)
            self.assertEqual(len(result['rows']), 10)
            self.assertEqual(result['rows'][0]['symbol'], 'NASDAQ:S11')
            self.assertEqual(result['excluded'][0]['symbol'], 'NASDAQ:MISSING')
            leader = result['rows'][0]
            self.assertAlmostEqual(leader['score'], sum(leader['rs'].values()) * 0.2 + leader['high_52w']['distance_pct'] * 0.2)
            self.assertIn('Top 10 market leaders', market_leaders_card(result))
            self.assertEqual(result['start_dates']['1W'], days[-6].isoformat())


if __name__ == '__main__':
    unittest.main()
