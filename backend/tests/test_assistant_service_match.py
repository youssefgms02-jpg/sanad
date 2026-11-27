import unittest
from types import SimpleNamespace

from assistant_service_match import resolve_assistant_service


def service(service_id, name, description="خدمة للمواطنين", category="government"):
    return SimpleNamespace(
        id=service_id,
        name=name,
        description=description,
        category=category,
        authority="جهة حكومية",
        eligibility="",
        documents="",
        steps="",
        fees="",
        processing_time="",
        application_methods="",
        follow_up="",
        appeals="",
        faqs="",
        practical_tips="",
    )


class AssistantServiceMatchTests(unittest.TestCase):
    def setUp(self):
        self.birth = service(1, "استخراج شهادة ميلاد مميكنة")
        self.death = service(2, "استخراج شهادة وفاة مميكنة")
        self.kindergarten = service(3, "تقديم رياض الأطفال", category="education")
        self.services = [self.birth, self.death, self.kindergarten]

    def test_explicitly_named_other_service_overrides_open_page(self):
        selected = resolve_assistant_service(
            self.services,
            "شهاده ميلاد",
            page_service=self.death,
        )
        self.assertEqual(selected.id, self.birth.id)

    def test_definite_article_variant_overrides_unrelated_page(self):
        selected = resolve_assistant_service(
            self.services,
            "عايز اوراق شهاده الميلاد",
            page_service=self.kindergarten,
        )
        self.assertEqual(selected.id, self.birth.id)

    def test_question_about_current_service_keeps_page_context(self):
        selected = resolve_assistant_service(
            self.services,
            "شهاده وفاه",
            page_service=self.death,
        )
        self.assertEqual(selected.id, self.death.id)

    def test_unrelated_follow_up_keeps_page_context(self):
        selected = resolve_assistant_service(
            self.services,
            "المستندات المطلوبه",
            page_service=self.kindergarten,
        )
        self.assertEqual(selected.id, self.kindergarten.id)

    def test_home_page_still_uses_ranked_search(self):
        selected = resolve_assistant_service(
            self.services,
            "شهاده الميلاد",
            page_service=None,
        )
        self.assertEqual(selected.id, self.birth.id)


if __name__ == "__main__":
    unittest.main()
