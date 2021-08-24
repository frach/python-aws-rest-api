from unittest import TestCase

from handlers import get_health


class HealthGetTestCase(TestCase):
    def test_get_health(self):
        response = get_health(None, None)
        self.assertEqual(response, {'headers': {'Content-Type': 'application/json'}, 'statusCode': 200})
