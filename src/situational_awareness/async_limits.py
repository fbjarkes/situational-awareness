"""Process-local async concurrency and rolling-window request limits."""
import asyncio
from collections import deque
from functools import wraps
import inspect
import math
from threading import Lock
import time


class AsyncCallLimiter:
    """Share one instance across async functions to share their call budget.

    Works as a decorator or `async with limiter`. Counts admitted calls, including
    failures/cancellations, in a rolling window. Waiting never blocks the event
    loop. Thread-protected state survives sequential asyncio.run() invocations;
    independent processes and connected tools outside Python have separate state.
    """

    def __init__(self, max_concurrent=3, max_calls=40, period_seconds=60):
        for value in (max_concurrent, max_calls):
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError("Concurrency and call limits must be positive integers")
        if not math.isfinite(period_seconds) or period_seconds <= 0:
            raise ValueError("period_seconds must be positive and finite")
        self.max_concurrent = max_concurrent
        self.max_calls = max_calls
        self.period_seconds = period_seconds
        self._lock = Lock()
        self._starts = deque()
        self._active = 0

    async def __aenter__(self):
        while True:
            with self._lock:
                now = time.monotonic()
                while self._starts and self._starts[0] <= now - self.period_seconds:
                    self._starts.popleft()
                if self._active < self.max_concurrent and len(self._starts) < self.max_calls:
                    self._active += 1
                    self._starts.append(now)
                    return self
                delay = 0.01 if self._active >= self.max_concurrent else self._starts[0] + self.period_seconds - now
            await asyncio.sleep(max(delay, 0.001))

    async def __aexit__(self, exc_type, exc, traceback):
        with self._lock:
            self._active -= 1

    def __call__(self, function):
        if not inspect.iscoroutinefunction(function):
            raise TypeError("AsyncCallLimiter decorates async functions only")

        @wraps(function)
        async def wrapped(*args, **kwargs):
            async with self:
                return await function(*args, **kwargs)
        return wrapped


# One budget for all TradingView market-data and earnings requests in this process.
TRADINGVIEW_LIMITER = AsyncCallLimiter(max_concurrent=3, max_calls=40, period_seconds=60)


@TRADINGVIEW_LIMITER
async def tradingview_call_tool(session, name, arguments):
    """Limit individual provider calls, including every historical-data page.

    Does not retry errors or mutations. Provider quota errors still propagate.
    """
    return await session.call_tool(name, arguments)
