import os
import unittest
from unittest.mock import patch

from assistant_web_search import search_web, is_official_hint


class AssistantWebSearchTests(unittest.TestCase):
    def test_returns_empty_when_api_key_is_not_configured(self):
        with patch.dict(os.environ, {"SANAD_TAVILY_API_KEY": ""}):
            self.assertEqual(search_web("تكافل وكرامة"), [])

    def test_official_domain_hint_checks_hostname_boundary(self):
        self.assertTrue(is_official_hint("https://www.moss.gov.eg/page"))
        self.assertTrue(is_official_hint("https://psm.gov.eg/services/1"))
        self.assertFalse(is_official_hint("https://moss.gov.eg.example.com/page"))
        self.assertFalse(is_official_hint("https://example.com/moss.gov.eg/page"))

    @patch("assistant_web_search.urlopen")
    def test_filters_non_official_results(self, mocked_urlopen):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return """{"results":[
                    {"title":"مقال عام","url":"https://example.com/info","content":"عام"},
                    {"title":"وزارة التضامن","url":"https://www.moss.gov.eg/page","content":"رسمي"}
                ]}""".encode("utf-8")

        mocked_urlopen.return_value = FakeResponse()
        with patch.dict(os.environ, {"SANAD_TAVILY_API_KEY": "test-key"}):
            results = search_web("تكافل وكرامة", count=2)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "وزارة التضامن")
        self.assertTrue(results[0]["official_hint"])


if __name__ == "__main__":
    unittest.main()
