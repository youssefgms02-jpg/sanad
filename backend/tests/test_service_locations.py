import unittest
from types import SimpleNamespace

from service_locations import map_search_url


class ServiceLocationsTests(unittest.TestCase):
    def test_map_search_url_uses_service_and_authority(self):
        service = SimpleNamespace(name="خدمة تجريبية", authority="جهة رسمية")
        url = map_search_url(service)
        self.assertIn("google.com/maps/search", url)
        self.assertIn("%D8%AE%D8%AF%D9%85%D8%A9", url)


if __name__ == "__main__":
    unittest.main()
