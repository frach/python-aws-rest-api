from unittest import TestCase

from src.main import health_get_endpoint


class HealthGetTestCase(TestCase):
    def test_get_health(self):
        response = health_get_endpoint(None, None)
        self.assertEqual(response, {'headers': {'Content-Type': 'application/json'}, 'statusCode': 200})
