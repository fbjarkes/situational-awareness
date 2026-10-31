from pathlib import Path
import unittest

from earnings_growth import quarterly_growth
from spy_earnings import revenue_streak, spy_holdings


class SpyEarningsTests(unittest.TestCase):
    def test_holdings_security_count(self):
        rows = spy_holdings(Path('knowledge/index/spy-holdings.md'))
        self.assertEqual(len(rows), 503)
        self.assertIn('BRK.B', {r['ticker'] for r in rows})

    def test_latest_two_yoy_quarters_and_strict_threshold(self):
        rows = [{'period_label': label, 'revenue': value, 'eps': -1} for label, value in
                [('Q1 2025', 100), ('Q2 2025', 100), ('Q1 2026', 130), ('Q2 2026', 140)]]
        growth = list(reversed(quarterly_growth(rows)))
        self.assertTrue(revenue_streak(growth))  # EPS losses do not exclude.
        growth[0]['revenue_yoy_pct'] = 25
        self.assertFalse(revenue_streak(growth))
        growth[0]['revenue_yoy_pct'] = None
        self.assertIsNone(revenue_streak(growth))
        growth[0]['period_label'] = 'Q4 2026'
        self.assertIsNone(revenue_streak(growth))

    def test_no_fallback_to_an_earlier_passing_streak(self):
        rows = [{'period_label': 'Q3 2026', 'revenue_yoy_pct': 10},
                {'period_label': 'Q2 2026', 'revenue_yoy_pct': 40},
                {'period_label': 'Q1 2026', 'revenue_yoy_pct': 50}]
        self.assertFalse(revenue_streak(rows))


if __name__ == '__main__':
    unittest.main()
