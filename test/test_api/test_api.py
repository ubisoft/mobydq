"""Unit tests for API components."""
from datetime import datetime
import requests
import time
import unittest


class TestApi(unittest.TestCase):
    """Unit tests for API components."""

    @classmethod
    def setUpClass(self):
        """Execute this before the tests."""
        self.base_url = 'http://api:5434/mobydq/api/v1'

    @staticmethod
    def get_test_case_name():
        """Generate unique name for unit test case."""

        time.sleep(1)
        test_case_name = 'test {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return test_case_name

    def test_get_health(self):
        """Unit tests endpoint get /health."""

        url = self.base_url + '/health'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        status = response.status_code

        # Assert http status code is 200
        self.assertEqual(status, 200)

    @classmethod
    def tearDownClass(self):
        """Execute this at the end of the tests."""
        pass


if __name__ == '__main__':
    unittest.main()
