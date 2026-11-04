from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

from situational_awareness.earnings import cache_path, download_earnings, request_window, save_earnings_response


def response():
    return {"success": True, "symbol": "NASDAQ:MSFT", "period": "fq",
            "labels": ["Q1 2025", "Q1 2025"], "series": {
                "revenue": [{"value": 100, "yoy_pct": 10}, {"value": 120, "yoy_pct": None}],
                "eps": [{"value": -1.5}, {"value": None}]}}


class EarningsTests(unittest.TestCase):
    def test_readable_cache_keeps_duplicates_missing_values_and_metadata(self):
        with tempfile.TemporaryDirectory(dir="reports") as folder:
            root = Path(folder)
            fetch = Mock(return_value=response())
            first = download_earnings('NASDAQ:MSFT', end='2026-10-31', data_root=root, fetcher=fetch)
            second = download_earnings('NASDAQ:MSFT', end='2026-10-31', data_root=root, fetcher=fetch)
            self.assertEqual(first, second)
            self.assertEqual(fetch.call_count, 1)
            self.assertEqual(first['quarters'][0]['eps'], -1.5)
            self.assertIsNone(first['quarters'][1]['eps'])
            self.assertEqual(first['observation_count'], 2)
            self.assertEqual(first['unique_period_labels'], 1)
            self.assertTrue(any('Duplicate' in w for w in first['warnings']))
            self.assertIsNone(first['currency'])
            self.assertIn('\n  "schema_version"', cache_path('NASDAQ:MSFT', root).read_text(encoding='utf-8'))
            self.assertEqual(first['provider_response'], response())

    def test_refresh_and_window_changes_refetch_but_age_does_not(self):
        with tempfile.TemporaryDirectory(dir="reports") as folder:
            root, fetch = Path(folder), Mock(return_value=response())
            for options in ({}, {'refresh': True}, {'years': 3}):
                download_earnings('NASDAQ:MSFT', end='2026-10-31', data_root=root, fetcher=fetch, **options)
            self.assertEqual(fetch.call_count, 3)
            path = cache_path('NASDAQ:MSFT', root)
            cached = json.loads(path.read_text())
            cached['fetched_at'] = (datetime.now(timezone.utc) - timedelta(days=3650)).isoformat()
            path.write_text(json.dumps(cached))
            download_earnings('NASDAQ:MSFT', years=3, end='2026-10-31', data_root=root, fetcher=fetch)
            self.assertEqual(fetch.call_count, 3)

    def test_failed_or_misaligned_response_preserves_prior_cache(self):
        with tempfile.TemporaryDirectory(dir="reports") as folder:
            root = Path(folder)
            download_earnings('NASDAQ:MSFT', data_root=root, fetcher=lambda *a: response())
            path = cache_path('NASDAQ:MSFT', root)
            previous = path.read_bytes()
            bad = response()
            bad['series']['eps'].pop()
            for invalid in (bad, {**response(), 'success': False}, {**response(), 'symbol': 'NASDAQ:OTHER'}):
                with self.assertRaises(ValueError):
                    download_earnings('NASDAQ:MSFT', data_root=root, refresh=True, fetcher=lambda *a: invalid)
                self.assertEqual(previous, path.read_bytes())

    def test_stockholm_download_date_and_leap_year_window(self):
        self.assertEqual(request_window(1, '2024-02-29'), (date(2023, 2, 28), date(2024, 2, 29)))
        with tempfile.TemporaryDirectory(dir="reports") as folder:
            payload = save_earnings_response('NASDAQ:MSFT', response(), start=date(2021, 10, 31),
                                             end=date(2026, 10, 31), fetched_at='2026-10-30T23:30:00Z', data_root=Path(folder))
            self.assertEqual(payload['download_date'], '2026-10-31')
        with self.assertRaises(ValueError):
            cache_path('MSFT')


if __name__ == '__main__':
    unittest.main()
