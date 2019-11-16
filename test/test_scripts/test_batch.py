"""Unit tests for module /scripts/init/batch.py."""
import unittest
from shared.utils import get_test_case_name, get_authorization
from scripts.batch import Batch
from scripts import utils


class TestBatch(unittest.TestCase):
    """Unit tests for class Batch."""

    def test_update_batch_status(self):
        """Unit tests for method update_batch_status."""

        # Authenticate user
        authorization = get_authorization()

        # Create test indicator group
        test_case_name = get_test_case_name()
        mutation_create_indicator_group = 'mutation{createIndicatorGroup(input:{indicatorGroup:{name:"test_case_name"}}){indicatorGroup{id}}}'
        mutation_create_indicator_group = mutation_create_indicator_group.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator_group = {'query': mutation_create_indicator_group}  # Convert to dictionary
        indicator_group = utils.execute_graphql_request(authorization, mutation_create_indicator_group)
        indicator_group_id = indicator_group['data']['createIndicatorGroup']['indicatorGroup']['id']

        # Create test batch
        mutation_create_batch = 'mutation{createBatch(input:{batch:{indicatorGroupId:indicator_group_id,status:"Pending"}}){batch{id}}}'
        mutation_create_batch = mutation_create_batch.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        mutation_create_batch = {'query': mutation_create_batch}  # Convert to dictionary
        batch = utils.execute_graphql_request(authorization, mutation_create_batch)
        batch_id = batch['data']['createBatch']['batch']['id']

        # Update test batch status
        batch = Batch()
        data = batch.update_batch_status(authorization, batch_id, 'Running')
        batch_status = data['data']['updateBatchById']['batch']['status']

        # Assert batch status is Running
        self.assertEqual(batch_status, 'Running')


if __name__ == '__main__':
    unittest.main()
