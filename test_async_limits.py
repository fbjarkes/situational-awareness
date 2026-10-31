import asyncio
import time
import unittest

from async_limits import AsyncCallLimiter


class AsyncLimitTests(unittest.TestCase):
    def test_shared_decorators_bound_concurrent_calls(self):
        async def run():
            limiter = AsyncCallLimiter(max_concurrent=2, max_calls=100)
            active = peak = 0
            @limiter
            async def work(value):
                nonlocal active, peak
                active += 1
                peak = max(peak, active)
                await asyncio.sleep(.005)
                active -= 1
                return value
            @limiter
            async def other(value):
                return await asyncio.sleep(.005, result=value)
            result = await asyncio.gather(*(work(i) for i in range(6)), other(9))
            self.assertEqual(result, [0, 1, 2, 3, 4, 5, 9])
            self.assertEqual(peak, 2)
            self.assertEqual(work.__name__, 'work')
        asyncio.run(run())

    def test_rate_budget_survives_separate_event_loops(self):
        limiter = AsyncCallLimiter(max_calls=2, period_seconds=.04)
        starts = []
        @limiter
        async def work():
            starts.append(time.monotonic())
        asyncio.run(work())
        asyncio.run(work())
        asyncio.run(work())
        self.assertGreaterEqual(starts[2] - starts[0], .039)

    def test_cancellation_and_failure_release_concurrency(self):
        async def run():
            limiter = AsyncCallLimiter(max_concurrent=1, max_calls=10)
            entered = asyncio.Event()
            @limiter
            async def hold():
                entered.set()
                await asyncio.Event().wait()
            task = asyncio.create_task(hold())
            await entered.wait()
            waiting = asyncio.create_task(hold())
            await asyncio.sleep(0)
            waiting.cancel()
            task.cancel()
            await asyncio.gather(task, waiting, return_exceptions=True)
            @limiter
            async def fail():
                raise ValueError('expected')
            with self.assertRaises(ValueError):
                await asyncio.wait_for(fail(), .2)
            async with limiter:
                self.assertEqual(limiter._active, 1)
            self.assertEqual(limiter._active, 0)
        asyncio.run(run())

    def test_invalid_settings(self):
        for kwargs in ({'max_calls': 0}, {'max_concurrent': -1}, {'period_seconds': float('inf')}):
            with self.assertRaises(ValueError):
                AsyncCallLimiter(**kwargs)
        with self.assertRaises(TypeError):
            AsyncCallLimiter()(lambda: None)


if __name__ == '__main__':
    unittest.main()
