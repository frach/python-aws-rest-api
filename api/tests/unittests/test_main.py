from unittest import TestCase

from main import get_health


class HealthGetTestCase(TestCase):
    def test_get_health(self):
        response = get_health()
        self.assertEqual(response, {'status': 'OK'})


class MainHandlerTestCase(TestCase):
    def test_validation_error_raised(self):
        pass
