import unittest
from types import SimpleNamespace

from fastapi import HTTPException

from service_rules import validate_official_source, validate_service_for_publish


class ServiceRulesTests(unittest.TestCase):
    def test_rejects_missing_source(self):
        with self.assertRaises(HTTPException):
            validate_official_source("")

    def test_rejects_http_source(self):
        with self.assertRaises(HTTPException):
            validate_official_source("http://example.gov.eg/service")

    def test_accepts_complete_https_service(self):
        service = SimpleNamespace(
            authority="جهة رسمية",
            eligibility="شروط معلنة",
            documents="المستندات تختلف حسب الحالة",
            steps="اتبع الخطوات الرسمية",
            official_source="https://example.gov.eg/service",
        )
        validate_service_for_publish(service)

    def test_rejects_incomplete_service(self):
        service = SimpleNamespace(
            authority="جهة رسمية",
            eligibility=None,
            documents="المستندات",
            steps="الخطوات",
            official_source="https://example.gov.eg/service",
        )
        with self.assertRaises(HTTPException):
            validate_service_for_publish(service)


if __name__ == "__main__":
    unittest.main()
