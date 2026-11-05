from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import json
import asyncio
import tempfile
import unittest
from unittest.mock import patch

from situational_awareness.bar_store import save_bars
from situational_awareness.weekly_studies import update_gdx_breadth


class WeeklyStudiesTests(unittest.TestCase):
    def test_foreign_report_download_is_rejected_before_network_call(self):
        from situational_awareness.market_report import fetch_tradingview
        with patch("mcp.client.streamable_http.streamablehttp_client") as network:
            with self.assertRaisesRegex(ValueError, "only support US"):
                asyncio.run(fetch_tradingview("http://unused", date(2026, 11, 4), date(2025, 1, 1), ("ASX:NST",)))
            network.assert_not_called()

    def test_daily_does_not_read_bars_or_write_snapshot(self):
        with tempfile.TemporaryDirectory() as folder, patch("situational_awareness.weekly_studies.load_bars") as load:
            path = Path(folder) / "weekly.json"
            path.write_text("saved weekly snapshot", encoding="utf-8")
            result = update_gdx_breadth(weekly=False, knowledge=folder, symbol_map=folder,
                                       output=path, data_root=folder, provider="tradingview", cutoff=date(2026, 11, 4))
            load.assert_not_called()
            self.assertEqual(path.read_text(), "saved weekly snapshot")
            self.assertFalse(result["updated"])

    def test_weekly_recalculates_from_one_us_batch_with_provenance(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            def bars(up):
                return [{"t": int(datetime(2026, 8, 1, 14, tzinfo=timezone.utc).timestamp()) + i*86400,
                         "c": 100+i if up else 100-i} for i in range(65)]
            save_bars({"provider": "tradingview", "fetched_at": "2026-11-04T21:00:00Z",
                       "series": {"NYSE:NEM": bars(True), "NYSE:AEM": bars(False)}}, root / "bars")
            with patch("situational_awareness.weekly_studies.theme_universes", return_value=[
                    {"id": "gold-miners", "symbols": ["NYSE:NEM", "NYSE:AEM"]}]), patch(
                    "situational_awareness.weekly_studies.metadata", return_value={"holdings_snapshot": {"as_of": "2026-10-22"}}):
                result = update_gdx_breadth(weekly=True, knowledge=root, symbol_map=root / "map.json",
                    output=root / "weekly.json", data_root=root / "bars", provider="tradingview",
                    cutoff=date(2026, 11, 4), download_date="2026-11-04")
            saved = json.loads((root / "weekly.json").read_text())
            self.assertTrue(result["updated"])
            self.assertEqual(saved["cadence"], "weekly")
            self.assertEqual(len(saved["input_bar_files"]), 2)
            points = next(iter(saved["series"].values()))
            self.assertEqual(points[-1]["c"], 50)
            self.assertEqual(points[-1]["universe_size"], 2)
