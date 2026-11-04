from datetime import date, datetime, timezone
from pathlib import Path
import tempfile
import unittest

from situational_awareness.bar_store import save_bars
from situational_awareness.price_ratio import build_rspd_rsps, ratio_points, ratio_card


class PriceRatioTests(unittest.TestCase):
    def test_same_date_division_and_invalid_inputs_are_gaps(self):
        a, b, c = date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3)
        result = ratio_points({a: 20, b: 40, c: 30}, {a: 10, c: 0})
        self.assertEqual([p['value'] for p in result], [2, None, None])

    def test_cutoff_month_change_and_batch_provenance(self):
        with tempfile.TemporaryDirectory(dir='reports') as folder:
            root = Path(folder)
            def bars(values):
                return [{'t': int(datetime.fromisoformat(day+'T14:00:00+00:00').timestamp()), 'c': value}
                        for day, value in zip(('2026-10-01', '2026-11-01', '2026-11-04'), values)]
            save_bars({'provider': 'tradingview', 'fetched_at': '2026-11-04T20:00:00Z',
                       'series': {'AMEX:RSPD': bars([10, 20, 99]), 'AMEX:RSPS': bars([10, 10, 10])}}, root)
            result = build_rspd_rsps(date(2026, 11, 3), data_root=root)
            self.assertEqual(result['latest'], 2)
            self.assertEqual(result['as_of'], '2026-11-01')
            self.assertEqual(result['change_1m_pct'], 100)
            self.assertEqual(result['download_date'], '2026-11-04')
            self.assertEqual(len(result['input_bar_files']), 2)
            html = ratio_card(result)
            self.assertIn('RSPD / RSPS', html)
            self.assertIn('outperformed', html)
            self.assertNotIn('99.000', html)

    def test_missing_pair_is_unavailable(self):
        with tempfile.TemporaryDirectory(dir='reports') as folder:
            result = build_rspd_rsps(date(2026, 11, 4), data_root=Path(folder))
            self.assertIn('unavailable', result)
            self.assertIn('unavailable', ratio_card(result))


if __name__ == '__main__':
    unittest.main()
