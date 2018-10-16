"""Unit tests for API components."""
import json
import unittest
import requests


class TestApi(unittest.TestCase):
    """Unit tests for API components."""

    @classmethod
    def setUpClass(cls):
        """Execute this before the tests."""
        cls.base_url = 'http://api:5434/mobydq/api/v1'

    def test_get_health(self):
        """Unit tests endpoint get /health."""

        url = self.base_url + '/health'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        status = response.status_code
        body = json.loads(response.text)

        # Assert http status code is 200
        self.assertEqual(status, 200)
        self.assertIsNotNone(body['message'])


if __name__ == '__main__':
    unittest.main()
