import unittest

from source_utils import extract_http_urls, valid_http_url, normalize_arabic_text, repeated_detail_groups


class SourceUtilsTests(unittest.TestCase):
    def test_extracts_multiple_urls_and_escaped_newlines(self):
        value = "وزارة الداخلية: https://moi.gov.eg/page\\nمصدر آخر: https://psm.gov.eg/services"
        self.assertEqual(
            extract_http_urls(value),
            ["https://moi.gov.eg/page", "https://psm.gov.eg/services"],
        )

    def test_strips_trailing_arabic_punctuation(self):
        self.assertEqual(extract_http_urls("https://moi.gov.eg/page،"), ["https://moi.gov.eg/page"])

    def test_rejects_non_http_and_credentials(self):
        self.assertFalse(valid_http_url("javascript:alert(1)"))
        self.assertFalse(valid_http_url("https://user:pass@moi.gov.eg"))
        self.assertTrue(valid_http_url("https://moi.gov.eg/page"))

    def test_arabic_normalization(self):
        self.assertEqual(normalize_arabic_text("إِصْدارُ البِطاقة"), normalize_arabic_text("اصدار البطاقه"))

    def test_finds_repeated_boilerplate_without_modifying_records(self):
        rows = [
            {"id": i, "name": f"خدمة {i}", "category": "government", "eligibility": "نص عام متكرر " * 10}
            for i in range(3)
        ]
        groups = repeated_detail_groups(rows, fields=("eligibility",), minimum=3)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["count"], 3)


if __name__ == "__main__":
    unittest.main()
