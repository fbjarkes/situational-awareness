from datetime import date, datetime, timezone
from pathlib import Path
import tempfile
import unittest

from bar_store import save_bars
from price_utils import lowest_close


class SymbolPriceUtilsTests(unittest.TestCase):
    def test_stored_symbol_respects_as_of_and_window(self):
        Path("reports").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir="reports") as folder:
            root = Path(folder)
            bars = [{"t": int(datetime(2026, 10, day, tzinfo=timezone.utc).timestamp()), "c": close}
                    for day, close in ((20, 30), (21, 25), (22, 20), (23, 22))]
            save_bars({"provider": "tradingview", "fetched_at": "2026-10-26T10:00:00Z", "series": {"CBOE:VIX": bars}}, root)
            self.assertEqual(lowest_close("CBOE:VIX", 365, data_root=root), 0)
            self.assertEqual(lowest_close("CBOE:VIX", 365, data_root=root, as_of="2026-10-22"), 3)
            self.assertEqual(lowest_close("CBOE:VIX", 2, data_root=root, as_of=date(2026, 10, 22)), 2)


if __name__ == "__main__":
    unittest.main()
