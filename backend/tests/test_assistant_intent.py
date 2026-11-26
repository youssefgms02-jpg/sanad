import unittest

from assistant_intent import detect_requested_detail


class AssistantIntentTests(unittest.TestCase):
    def test_documents_request_is_narrow(self):
        self.assertEqual(
            detect_requested_detail("عايز المستندات"),
            ("documents", "المستندات المطلوبة"),
        )

    def test_papers_synonym_maps_to_documents(self):
        self.assertEqual(
            detect_requested_detail("ايه الاوراق المطلوبه"),
            ("documents", "المستندات المطلوبة"),
        )

    def test_eligibility_request_is_narrow(self):
        self.assertEqual(
            detect_requested_detail("عايز اعرف الشروط"),
            ("eligibility", "شروط الاستفادة"),
        )

    def test_steps_request_is_narrow(self):
        self.assertEqual(
            detect_requested_detail("قول لي خطوات الحصول على الخدمه"),
            ("steps", "خطوات الحصول على الخدمة"),
        )

    def test_general_question_has_no_narrow_intent(self):
        self.assertIsNone(detect_requested_detail("عايز اطلع بطاقه"))


if __name__ == "__main__":
    unittest.main()
