import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("breadth_study", Path(__file__).with_name("breadth-study.py"))
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


class EventStudyTests(unittest.TestCase):
    def test_crossing_equality_and_recrossing(self):
        prices = dict(zip(["a", "b", "c", "d", "e", "f"], [31, 30, 29, 28, 30, 29]))
        self.assertEqual(study.crossings(prices, 30), ["c", "f"])

    def test_session_horizon_and_immature_signal(self):
        days = [f"{i:03}" for i in range(205)]
        spy = {d: 100 + i for i, d in enumerate(days)}
        breadth = {d: 40 for d in days}
        breadth[days[1]] = 10
        breadth[days[-1]] = 10
        events, summary = study.study(spy, {"test": breadth})
        row = next(r for r in summary if r["threshold"] == 20 and r["horizon"] == 10)
        self.assertEqual(row["n"], 1)
        self.assertEqual(row["immature"], 1)
        self.assertAlmostEqual(row["mean_pct"], (111 / 101 - 1) * 100)
        event = next(e for e in events if e["threshold"] == 20 and e["horizon"] == 200)
        self.assertEqual(event["exit_date"], days[201])


if __name__ == "__main__":
    unittest.main()
