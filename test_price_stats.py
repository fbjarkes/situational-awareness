import unittest

from price_stats import (cons_days_above_ma, cons_days_below_ma, cons_down_days, cons_up_days,
                         distance_from_ma, sma, streak_is_lower_bound, lowest_close_period)


class PriceStatsTests(unittest.TestCase):
    def test_kma_compression(self):
        from price_stats import kma_compression
        self.assertEqual(kma_compression([10] * 200), 0)
        self.assertIsNone(kma_compression([10] * 199))
        self.assertAlmostEqual(kma_compression([1, 2, 3, 4], (2, 4)), 25)
        self.assertEqual(kma_compression([10, 20, 30, 40], (2, 4)),
                         kma_compression([1, 2, 3, 4], (2, 4)))
        for periods in ((), (5,), (5, 5), (0, 5), (True, 5)):
            with self.assertRaises(ValueError):
                kma_compression([10] * 200, periods)

    def test_52w_high_events_and_age(self):
        from price_stats import new_52w_high, days_since_52w_high
        self.assertIsNone(new_52w_high([10] * 252))
        self.assertTrue(new_52w_high([10] * 252 + [11]))
        self.assertFalse(new_52w_high([10] * 253))
        self.assertEqual(days_since_52w_high([10] * 252 + [11]), 0)
        self.assertEqual(days_since_52w_high([10] * 252 + [11, 11, 9]), 2)
        self.assertIsNone(days_since_52w_high([10] * 300))
        # A past breakout remains a valid event after leaving today's window.
        self.assertEqual(days_since_52w_high([1, 2, 3, 4, 3, 2, 1], 3), 3)
        self.assertTrue(new_52w_high([100, 1, 2, 3, 4], 3))
        for function in (new_52w_high, days_since_52w_high):
            self.assertIsNone(function([]))
            with self.assertRaises(ValueError):
                function([1, float('nan')])
            with self.assertRaises(ValueError):
                function([1, 2], 0)

    def test_lowest_close_period(self):
        self.assertEqual(lowest_close_period(list(range(365, 0, -1))), 365)
        self.assertEqual(lowest_close_period([10, 12, 11]), 2)
        self.assertEqual(lowest_close_period([12, 10, 11]), 0)
        self.assertEqual(lowest_close_period([12, 10, 10]), 0)
        self.assertEqual(lowest_close_period([10, 12, 10]), 2)
        self.assertEqual(lowest_close_period([12, 11, 10], 2), 2)
        self.assertEqual(lowest_close_period([12, 11, 10], 1), 0)
        self.assertEqual(lowest_close_period([]), 0)
        self.assertEqual(lowest_close_period([10]), 0)
        with self.assertRaises(ValueError):
            lowest_close_period([10, 9], 0)
    def test_down_and_up_streaks(self):
        self.assertEqual(cons_down_days([10, 12, 11, 10, 9]), 3)
        self.assertEqual(cons_down_days([10, 9, 9]), 0)  # unchanged close ends the streak
        self.assertEqual(cons_down_days([10, 9, 10]), 0)
        self.assertEqual(cons_down_days([10]), 0)
        self.assertEqual(cons_up_days([10, 9, 10, 11]), 2)

    def test_sma_and_distance(self):
        self.assertIsNone(sma([1, 2], 3))
        self.assertEqual(sma([1, 2, 3, 4], 2), 3.5)
        self.assertAlmostEqual(distance_from_ma([90, 100, 110], 3), 10.0)
        self.assertIsNone(distance_from_ma([1, 2], 3))

    def test_ma_streaks_include_current_close(self):
        closes = [10, 10, 10, 11, 12, 13]
        # SMA3 ending at 11: 10.33, 12: 11, 13: 12 -> three sessions above.
        self.assertEqual(cons_days_above_ma(closes, 3), 3)
        self.assertEqual(cons_days_below_ma(closes, 3), 0)
        self.assertEqual(cons_days_below_ma([13, 12, 11, 10], 2), 3)
        self.assertEqual(cons_days_above_ma([10, 10, 10], 3), 0)  # equal to SMA is neither
        self.assertEqual(cons_days_above_ma([1, 2], 3), 0)

    def test_lower_bound_when_history_is_exhausted(self):
        closes = [10, 11, 12, 13]
        streak = cons_days_above_ma(closes, 2)
        self.assertEqual(streak, 3)
        self.assertTrue(streak_is_lower_bound(closes, streak, 2))
        self.assertTrue(streak_is_lower_bound([3, 2, 1], cons_down_days([3, 2, 1])))
        self.assertFalse(streak_is_lower_bound([1, 3, 2, 1], cons_down_days([1, 3, 2, 1])))

    def test_rejects_invalid_input(self):
        with self.assertRaises(ValueError):
            cons_down_days([10, 0])
        with self.assertRaises(ValueError):
            sma([1, 2, 3], 0)


if __name__ == "__main__":
    unittest.main()
