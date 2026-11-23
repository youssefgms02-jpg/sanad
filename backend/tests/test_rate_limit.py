import unittest

from rate_limit import RateLimiter


class RateLimiterTests(unittest.TestCase):
    def test_blocks_after_limit_and_allows_after_window(self):
        limiter = RateLimiter()
        self.assertEqual(limiter.allow("key", limit=2, window_seconds=10, now=100), (True, 0))
        self.assertEqual(limiter.allow("key", limit=2, window_seconds=10, now=101), (True, 0))
        allowed, retry_after = limiter.allow("key", limit=2, window_seconds=10, now=102)
        self.assertFalse(allowed)
        self.assertGreaterEqual(retry_after, 1)
        self.assertEqual(limiter.allow("key", limit=2, window_seconds=10, now=111), (True, 0))

    def test_keys_are_isolated(self):
        limiter = RateLimiter()
        self.assertEqual(limiter.allow("first", limit=1, window_seconds=10, now=100), (True, 0))
        self.assertEqual(limiter.allow("second", limit=1, window_seconds=10, now=100), (True, 0))


if __name__ == "__main__":
    unittest.main()
