from datetime import date
import importlib.util
from pathlib import Path
import unittest

from breadth import calculate_breadth


class BreadthTests(unittest.TestCase):
    def test_warmup_equality_missing_and_no_forward_fill(self):
        prices = {"a": {"2026-01-01": 10, "2026-01-02": 20, "2026-01-03": 10},
                  "b": {"2026-01-01": 5, "2026-01-02": 5},
                  "c": {"2026-01-02": 5, "2026-01-03": 10}}
        result = calculate_breadth(["a", "b", "c", "absent"], prices, 2)
        bars = next(iter(result["series"].values()))
        self.assertIsNone(bars[0]["c"])
        self.assertEqual((bars[1]["above"], bars[1]["equal"], bars[1]["below"]), (1, 1, 0))
        self.assertEqual(bars[1]["c"], 50)
        self.assertEqual((bars[2]["above"], bars[2]["below"], bars[2]["unavailable"]), (1, 1, 2))
        self.assertEqual(result["universe"]["missing_symbols"], ["absent"])

    def test_start_filter_preserves_warmup_and_coverage_gate(self):
        prices = {"a": {"2026-01-01": 10, "2026-01-02": 20}}
        result = calculate_breadth(["a", "missing"], prices, 2, start="2026-01-02", min_coverage=.6)
        bars = next(iter(result["series"].values()))
        self.assertEqual(len(bars), 1)
        self.assertEqual(bars[0]["above"], 1)
        self.assertIsNone(bars[0]["c"])

    def test_invalid_inputs(self):
        for window in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                calculate_breadth(["a"], {}, window)
        with self.assertRaises(ValueError):
            calculate_breadth(["a"], {"a": {"2026-01-01": float("nan")}}, 1)

    def test_gdx_universe_excludes_cash(self):
        spec = importlib.util.spec_from_file_location("custom_breadth", Path(__file__).with_name("custom-breadth.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        symbols = module.holdings_symbols(Path(__file__).parent / "knowledge/sectors/gdx.md")
        self.assertEqual(len(symbols), 59)
        self.assertIn("PE&OLES* MM", symbols)
        self.assertEqual(len(set(symbols)), 59)
        self.assertFalse(any("CASH" in s for s in symbols))
        snapshot = {"provider": "tradingview", "series": {"ASX:NST": [{"t": 1792706400, "c": 24.16}]}}
        self.assertIn("2026-10-23", module.prices_from_snapshot(snapshot)["ASX:NST"])


if __name__ == "__main__":
    unittest.main()
