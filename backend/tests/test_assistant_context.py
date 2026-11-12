import unittest
from types import SimpleNamespace

from assistant_context import DISCLAIMER, build_assistant_context


class AssistantContextTests(unittest.TestCase):
    def setUp(self):
        self.service = SimpleNamespace(
            id=64,
            name="خدمة تجريبية",
            description="وصف الخدمة",
            category="support",
            authority="جهة رسمية",
            eligibility="شروط",
            documents="مستندات",
            steps="خطوات",
            official_source="https://example.gov.eg/service",
            last_reviewed=None,
            status="published",
            created_at=None,
        )

    def test_service_context_contains_only_public_service_data(self):
        result = build_assistant_context(service=self.service)
        self.assertEqual(result["page_type"], "service")
        self.assertEqual(result["service"]["id"], 64)
        self.assertEqual(result["disclaimer"], DISCLAIMER)
        self.assertNotIn("password_hash", result)

    def test_home_context_does_not_claim_a_service(self):
        result = build_assistant_context()
        self.assertEqual(result["page_type"], "home")
        self.assertIsNone(result["service"])


if __name__ == "__main__":
    unittest.main()
