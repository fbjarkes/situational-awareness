from pathlib import Path
import tempfile
import unittest

from bar_store import save_bars, load_bars, symbol_filename


class BarStoreTests(unittest.TestCase):
    def payload(self, symbol="NYSE:NEM", fetched="2026-10-24T22:30:00Z", bars=None):
        return {"provider": "tradingview", "fetched_at": fetched,
                "series": {symbol: bars if bars is not None else [{"t": 1, "c": 10}]}}

    def test_roundtrip_download_date_and_windows_safe_name(self):
        Path('reports').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir='reports') as folder:
            root = Path(folder)
            paths = save_bars(self.payload(), root)
            self.assertEqual(paths[0].parent.name, "2026-10-25")
            self.assertEqual(paths[0].name, "NYSE%3ANEM.json")
            self.assertNotEqual(symbol_filename("A:B"), symbol_filename("A-B"))
            result = load_bars(["NYSE:NEM"], root)
            self.assertEqual(result["series"]["NYSE:NEM"][0]["c"], 10)
            self.assertEqual(len(result["bar_files"]), 1)

    def test_merge_preserves_long_history_and_latest_value(self):
        Path('reports').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir='reports') as folder:
            root = Path(folder)
            save_bars(self.payload(bars=[{"t": 1, "c": 10}, {"t": 2, "c": 20}]), root)
            save_bars(self.payload(fetched="2026-10-25T10:00:00Z", bars=[{"t": 2, "c": 21}]), root)
            save_bars(self.payload(fetched="2026-10-25T09:00:00Z", bars=[{"t": 2, "c": 19}, {"t": 0, "c": 5}]), root)
            result = load_bars(["NYSE:NEM"], root)
            self.assertEqual(result["series"]["NYSE:NEM"], [{"t": 0, "c": 5}, {"t": 1, "c": 10}, {"t": 2, "c": 21}])
            self.assertEqual(result["fetched_at"], "2026-10-25T10:00:00Z")

    def test_latest_complete_batch_does_not_mix_dates(self):
        Path('reports').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir='reports') as folder:
            root = Path(folder)
            save_bars(self.payload(), root)
            save_bars(self.payload(symbol="NYSE:AEM"), root)
            save_bars(self.payload(fetched="2026-10-26T10:00:00Z"), root)
            self.assertEqual(load_bars(["NYSE:NEM", "NYSE:AEM"], root)["download_date"], "2026-10-25")
            with self.assertRaises(ValueError):
                load_bars(["NYSE:NEM", "NYSE:AEM"], root, download_date="2026-10-26")


if __name__ == "__main__":
    unittest.main()
