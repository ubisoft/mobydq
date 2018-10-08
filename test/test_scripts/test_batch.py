"""Unit tests for module /scripts/init/batch.py."""
from datetime import datetime
from scripts.batch import Batch
from scripts import utils
import time
import unittest


class TestBatch(unittest.TestCase):
    """Unit tests for class Batch."""

    @classmethod
    def setUpClass(self):
        """Execute this before the tests."""
        pass

    @staticmethod
    def get_test_case_name():
        """Generate unique name for unit test case."""

        time.sleep(1)
        test_case_name = 'test {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return test_case_name

    def test_update_batch_status(self):
        """Unit tests for method update_batch_status."""

        # Create test indicator group
        test_case_name = TestBatch.get_test_case_name()
        mutation_create_indicator_group = '''mutation{createIndicatorGroup(input:{indicatorGroup:{name:"test_case_name"}}){indicatorGroup{id}}}'''
        mutation_create_indicator_group = mutation_create_indicator_group.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        indicator_group = utils.execute_graphql_request(mutation_create_indicator_group)
        indicator_group_id = indicator_group['data']['createIndicatorGroup']['indicatorGroup']['id']

        # Create test batch
        mutation_create_batch = '''mutation{createBatch(input:{batch:{indicatorGroupId:indicator_group_id,status:"Pending"}}){batch{id}}}'''
        mutation_create_batch = mutation_create_batch.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        batch = utils.execute_graphql_request(mutation_create_batch)
        batch_id = batch['data']['createBatch']['batch']['id']

        # Update test batch status
        batch = Batch()
        data = batch.update_batch_status(batch_id, 'Running')
        batch_status = data['data']['updateBatchById']['batch']['status']

        # Assert batch status is Running
        self.assertEqual(batch_status, 'Running')

    @classmethod
    def tearDownClass(self):
        """Execute this at the end of the tests."""
        pass


if __name__ == '__main__':
    unittest.main()
