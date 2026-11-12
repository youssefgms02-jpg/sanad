import unittest
from datetime import datetime, timezone
from types import SimpleNamespace

from service_catalog import search_score, service_to_dict


class ServiceCatalogTests(unittest.TestCase):
    def setUp(self):
        self.service = SimpleNamespace(
            id=64,
            name="استخراج بدل فاقد لبطاقة التموين",
            description="إصدار بطاقة بديلة عند الفقد",
            category="support",
            authority="وزارة التموين والتجارة الداخلية",
            eligibility="مالك البطاقة",
            documents="لا توجد مستندات",
            steps="تقديم الطلب في مكتب التموين",
            official_source="https://digital.gov.eg/service",
            last_reviewed=datetime(2026, 11, 11, tzinfo=timezone.utc),
            status="published",
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

    def test_serializes_public_fields_and_extracts_source(self):
        data = service_to_dict(self.service)
        self.assertEqual(data["id"], 64)
        self.assertEqual(data["source_urls"], ["https://digital.gov.eg/service"])
        self.assertEqual(data["status"], "published")
        self.assertNotIn("password", data)

    def test_name_match_ranks_above_unrelated_text(self):
        self.assertGreater(search_score(self.service, "بدل فاقد"), 0)
        self.assertEqual(search_score(self.service, "سيارة"), 0)

    def test_serialization_includes_freshness_metadata(self):
        data = service_to_dict(self.service)
        self.assertIn(data["freshness"]["status"], {"fresh", "stale"})
        self.assertEqual(data["freshness"]["max_age_days"], 20)


if __name__ == "__main__":
    unittest.main()
