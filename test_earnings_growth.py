import unittest
from earnings_growth import quarterly_growth, growth_pct
from report_design import earnings_growth_card


class EarningsGrowthTests(unittest.TestCase):
    def test_same_quarter_prior_year_and_nonpositive_eps_base(self):
        rows = [{'period_label': 'Q1 2025', 'revenue': 100, 'eps': -1},
                {'period_label': 'Q1 2026', 'revenue': 120, 'eps': 2},
                {'period_label': 'Q1 2027', 'revenue': 90, 'eps': 1}]
        result = quarterly_growth(rows)
        self.assertAlmostEqual(result[1]['revenue_yoy_pct'], 20)
        self.assertIsNone(result[1]['eps_yoy_pct'])
        self.assertAlmostEqual(result[2]['revenue_yoy_pct'], -25)
        self.assertAlmostEqual(result[2]['eps_yoy_pct'], -50)
        self.assertIsNone(growth_pct(100, 0))

    def test_duplicate_labels_and_gaps_do_not_create_quarterly_growth(self):
        rows = [{'period_label': label, 'revenue': 100, 'eps': 1} for label in
                ['Q1 2025', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q1 2026']]
        self.assertTrue(all(row['revenue_yoy_pct'] is None for row in quarterly_growth(rows)))

    def test_one_row_per_company_with_escaped_labels(self):
        row = {'symbol': '<SYMBOL>', 'quarters': quarterly_growth([
            {'period_label': 'Q1 2025', 'revenue': 200000000, 'eps': 1},
            {'period_label': 'Q1 2026', 'revenue': 240000000, 'eps': 2}]), 'warnings': []}
        html = earnings_growth_card({'rows': [row], 'columns': 2, 'available': 1, 'interpretation': 'Example'})
        self.assertEqual(html.count('<tr>'), 2)
        self.assertIn('&lt;SYMBOL&gt;', html)
        self.assertIn('+20.0%', html)
        self.assertIn('+100.0%', html)
        self.assertIn('(240.0M)', html)
        self.assertIn('(2.00)', html)


if __name__ == '__main__':
    unittest.main()
