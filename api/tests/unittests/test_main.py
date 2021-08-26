from unittest import TestCase

from main import get_health


class HealthGetTestCase(TestCase):
    def test_get_health(self):
        response = get_health()
        self.assertEqual(response, {'status': 'OK'})
