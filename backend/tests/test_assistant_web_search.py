import os
import unittest
from unittest.mock import patch

from assistant_web_search import search_web


class AssistantWebSearchTests(unittest.TestCase):
    def test_returns_empty_when_api_key_is_not_configured(self):
        with patch.dict(os.environ, {"SANAD_BRAVE_SEARCH_API_KEY": ""}):
            self.assertEqual(search_web("تكافل وكرامة"), [])

    @patch("assistant_web_search.urlopen")
    def test_prioritizes_official_egyptian_domains(self, mocked_urlopen):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return (
                    b'{"web":{"results":['
                    b'{"title":"مقال عام","url":"https://example.com/info","description":"عام"},'
                    b'{"title":"وزارة التضامن","url":"https://www.moss.gov.eg/page","description":"رسمي"}'
                    b']}}'
                )

        mocked_urlopen.return_value = FakeResponse()
        with patch.dict(os.environ, {"SANAD_BRAVE_SEARCH_API_KEY": "test-key"}):
            results = search_web("تكافل وكرامة", count=2)

        self.assertEqual(results[0]["title"], "وزارة التضامن")
        self.assertTrue(results[0]["official_hint"])
        self.assertEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
