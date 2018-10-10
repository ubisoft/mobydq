"""Unit tests for module /scripts/init/utils.py."""
from scripts import utils
import unittest


class TestUtils(unittest.TestCase):
    """Unit tests for utility methods."""

    @classmethod
    def setUpClass(self):
        """Execute this before the tests."""
        pass

    def test_get_parameter(self):
        """Unit tests for method get_parameter."""

        api = utils.get_parameter('graphql')
        url = utils.get_parameter('graphql', 'url')

        # Assert parameters are not empty
        self.assertGreater(len(api), 0)
        self.assertGreater(len(url), 0)

    def test_execute_graphql_request(self):
        """Unit tests for method execute_graphql_request."""

        payload = 'query{allDataSourceTypes{nodes{id}}}'
        data = utils.execute_graphql_request(payload)
        nb_records = len(data['data']['allDataSourceTypes']['nodes'])

        # Assert graphql query returned records
        self.assertGreater(nb_records, 0)

    @classmethod
    def tearDownClass(self):
        """Execute this at the end of the tests."""
        pass


if __name__ == '__main__':
    unittest.main()
