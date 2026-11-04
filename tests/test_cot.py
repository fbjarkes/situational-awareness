from datetime import date, datetime
from pathlib import Path
import unittest

from situational_awareness.cot import GROUPS, parse_history, build_cot_section, futures_session_date
from situational_awareness.cot_design import cot_chart


def row(code='13874+', observed='2026-10-27'):
    data = {'CFTC_Contract_Market_Code': code, 'Report_Date_as_YYYY-MM-DD': observed, 'Open_Interest_All': '1000'}
    for _, prefix, _ in GROUPS.values():
        data[prefix + '_Positions_Long_All'] = '100'
        data[prefix + '_Positions_Short_All'] = '100'
    return data


class CotTests(unittest.TestCase):
    def test_cme_overnight_session_labels_across_dst(self):
        self.assertEqual(futures_session_date(datetime.fromisoformat('2026-11-03T23:00:00+00:00').timestamp()), date(2026, 11, 4))
        self.assertEqual(futures_session_date(datetime.fromisoformat('2026-07-06T22:00:00+00:00').timestamp()), date(2026, 7, 7))
        self.assertEqual(futures_session_date(datetime.fromisoformat('2026-07-07T14:00:00+00:00').timestamp()), date(2026, 7, 7))

    def test_net_positions_and_contract_scope(self):
        data = row()
        data['Asset_Mgr_Positions_Long_All'] = '150'
        data['Dealer_Positions_Short_All'] = '150'
        parsed = parse_history([data, row('20974+'), row('13874A')])
        self.assertEqual(parsed['13874+'][0]['groups']['asset_managers']['net'], 50)
        self.assertEqual(parsed['13874+'][0]['groups']['dealers']['net'], -50)
        self.assertEqual(len(parsed['13874+']), 1)

    def test_conflicts_and_reconciliation(self):
        data = row()
        data['Dealer_Positions_Long_All'] = '102'
        self.assertEqual(parse_history([data])['13874+'][0]['net_reconciliation_residual'], 2)
        with self.assertRaises(ValueError):
            parse_history([row(), data])
        data['Dealer_Positions_Long_All'] = '200'
        with self.assertRaises(ValueError):
            parse_history([data])

    def test_absent_history_is_unavailable(self):
        self.assertIn('unavailable', build_cot_section(date(2026, 11, 4), root=Path('reports/no-cot-fixture')))

    def test_signed_bars_and_separate_price_panel(self):
        point = parse_history([row()])['13874+'][0]
        market = {'title': 'S&P 500', 'start': '2026-01-01', 'end': '2026-11-04',
                  'prices': [{'date': '2026-10-27', 'o': 100, 'h': 102, 'l': 99, 'c': 101}], 'points': [point]}
        svg = cot_chart(market)
        self.assertIn('Daily futures price', svg)
        self.assertIn('Weekly net positions', svg)
        self.assertEqual(svg.count('class="cot-series"'), 5)
        self.assertIn('2026-10-27', svg)


if __name__ == '__main__':
    unittest.main()
