"""Process-local rate limiting for sensitive endpoints.

This is intentionally conservative and dependency-free. Production deployments with
multiple workers should replace the store with a shared Redis-backed limiter.
"""
from collections import defaultdict, deque
from threading import Lock
from time import monotonic


class RateLimiter:
    def __init__(self):
        self._events = defaultdict(deque)
        self._lock = Lock()

    def allow(self, key, *, limit, window_seconds, now=None):
        current = monotonic() if now is None else now
        cutoff = current - window_seconds
        with self._lock:
            events = self._events[key]
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= limit:
                retry_after = max(1, int(events[0] + window_seconds - current))
                return False, retry_after
            events.append(current)
            return True, 0


limiter = RateLimiter()


def client_key(request, bucket):
    host = request.client.host if request.client else "unknown"
    return f"{bucket}:{host}"
