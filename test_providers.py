import importlib.util
import io
import json
import os
from argparse import Namespace
from datetime import date
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from bar_store import load_bars, save_bars
from providers import alpaca_symbol, fetch_alpaca_daily

spec = importlib.util.spec_from_file_location("custom_breadth", Path(__file__).with_name("custom-breadth.py"))
custom = importlib.util.module_from_spec(spec)
spec.loader.exec_module(custom)

CREDS = {"APCA_API_KEY_ID": "key", "APCA_API_SECRET_KEY": "secret"}


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def bar(day, close):
    return {"t": f"2026-10-{day:02}T04:00:00Z", "o": close, "h": close, "l": close, "c": close, "v": 100}


class AlpacaProviderTests(unittest.TestCase):
    def test_symbol_mapping_excludes_indices_and_foreign_listings(self):
        self.assertEqual(alpaca_symbol("NYSE:NEM"), "NEM")
        self.assertEqual(alpaca_symbol("AMEX:SPY"), "SPY")
        self.assertEqual(alpaca_symbol("NEM"), "NEM")
        self.assertIsNone(alpaca_symbol("INDEX:MMOH"))
        self.assertIsNone(alpaca_symbol("TSX:LUG"))
        self.assertIsNone(alpaca_symbol("NST AU"))

    def test_fetch_pages_and_reports_empty_symbols(self):
        pages = [{"bars": {"NEM": [bar(22, 10)]}, "next_page_token": "p2"},
                 {"bars": {"NEM": [bar(23, 11)]}, "next_page_token": None}]
        requests = []

        def opener(request, timeout):
            requests.append(request)
            return FakeResponse(json.dumps(pages[len(requests) - 1]).encode())

        with mock.patch.dict(os.environ, CREDS):
            payload = fetch_alpaca_daily(["NEM", "ZZZZ"], date(2026, 10, 1), opener=opener)
        self.assertIn("page_token=p2", requests[1].full_url)
        self.assertEqual(requests[0].get_header("Apca-api-key-id"), "key")
        self.assertEqual([b["c"] for b in payload["series"]["NEM"]], [10, 11])
        self.assertEqual(payload["empty_symbols"], ["ZZZZ"])
        self.assertEqual(payload["provider"], "alpaca")
        self.assertNotIn("secret", json.dumps(payload))

    def test_missing_credentials_fail(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "APCA_API_KEY_ID"):
                fetch_alpaca_daily(["NEM"], date(2026, 10, 1), opener=None)

    def test_store_selects_by_provider_and_custom_breadth_marks_unavailable(self):
        Path("reports").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir="reports") as folder:
            root = Path(folder)
            bars = [{"t": 1761192000 + 86400 * i, "c": 10.0 + i} for i in range(3)]
            save_bars({"provider": "alpaca", "fetched_at": "2026-10-25T10:00:00Z", "feed": "iex",
                       "adjustment": "split", "session_timezones": {"NEM": "America/New_York"},
                       "series": {"NEM": bars}}, root)
            save_bars({"provider": "tradingview", "fetched_at": "2026-10-26T10:00:00Z",
                       "series": {"NEM": bars}}, root)
            self.assertEqual(load_bars(["NEM"], root, provider="alpaca")["download_date"], "2026-10-25")
            self.assertEqual(load_bars(["NEM"], root)["download_date"], "2026-10-26")
            with self.assertRaisesRegex(ValueError, "Feed conflict"):
                save_bars({"provider": "alpaca", "fetched_at": "2026-10-25T11:00:00Z", "feed": "sip",
                           "adjustment": "split", "series": {"NEM": bars}}, root)
            args = Namespace(alpaca=False, data_root=root, download_date=None)
            source, prices, unavailable = custom.alpaca_source(["NYSE:NEM", "TSX:LUG"], args)
            self.assertEqual(source["feed"], "iex")
            self.assertEqual(list(prices), ["NYSE:NEM"])
            self.assertIn("US-listed", unavailable["TSX:LUG"])


if __name__ == "__main__":
    unittest.main()
