"""Unit tests for module /scripts/init/utils.py."""
import unittest
from scripts import utils


class TestUtils(unittest.TestCase):
    """Unit tests for utility methods."""

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
        payload = {'query': payload}  # Convert to dictionary
        #data = utils.execute_graphql_request(None, payload)
        #nb_records = len(data['data']['allDataSourceTypes']['nodes'])

        # Assert graphql query returned records
        #self.assertGreater(nb_records, 0)


if __name__ == '__main__':
    unittest.main()
