"""Unit tests for module /scripts/init/session.py."""
import unittest
from shared.utils import get_test_case_name, get_authorization
from scripts.session import Session
from scripts import utils


class TestSession(unittest.TestCase):
    """Unit tests for class Session."""

    def test_update_session_status(self):
        """Unit tests for method update_session_status."""

        # Authenticate user
        authorization = get_authorization()

        # Create test indicator group
        test_case_name = get_test_case_name()
        mutation_create_indicator_group = 'mutation{createIndicatorGroup(input:{indicatorGroup:{name:"test_case_name"}}){indicatorGroup{id}}}'
        mutation_create_indicator_group = mutation_create_indicator_group.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator_group = {'query': mutation_create_indicator_group}  # Convert to dictionary
        indicator_group = utils.execute_graphql_request(authorization, mutation_create_indicator_group)
        indicator_group_id = indicator_group['data']['createIndicatorGroup']['indicatorGroup']['id']

        # Create test indicator
        mutation_create_indicator = 'mutation{createIndicator(input:{indicator:{name:"test_case_name",flagActive:true,indicatorTypeId:1,indicatorGroupId:indicator_group_id}}){indicator{id}}}'
        mutation_create_indicator = mutation_create_indicator.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = {'query': mutation_create_indicator}  # Convert to dictionary
        indicator = utils.execute_graphql_request(authorization, mutation_create_indicator)
        indicator_id = indicator['data']['createIndicator']['indicator']['id']

        # Create test batch
        mutation_create_batch = 'mutation{createBatch(input:{batch:{indicatorGroupId:indicator_group_id,,status:"Pending"}}){batch{id}}}'
        mutation_create_batch = mutation_create_batch.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        mutation_create_batch = {'query': mutation_create_batch}  # Convert to dictionary
        batch = utils.execute_graphql_request(authorization, mutation_create_batch)
        batch_id = batch['data']['createBatch']['batch']['id']

        # Create test session
        mutation_create_session = 'mutation{createSession(input:{session:{indicatorId:indicator_id,,batchId:batch_id,status:"Pending"}}){session{id}}}'
        mutation_create_session = mutation_create_session.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
        mutation_create_session = mutation_create_session.replace('batch_id', str(batch_id))  # Use replace() instead of format() because of curly braces
        mutation_create_session = {'query': mutation_create_session}  # Convert to dictionary
        session = utils.execute_graphql_request(authorization, mutation_create_session)
        session_id = session['data']['createSession']['session']['id']

        # Update test session status
        data = Session().update_session_status(authorization, session_id, 'Running')
        session_status = data['data']['updateSessionById']['session']['status']

        # Assert batch status is Running
        self.assertEqual(session_status, 'Running')

    # def test_compute_session_result(self):
        # """Unit tests for method compute_session_result."""
        # TODO:
        # pass


if __name__ == '__main__':
    unittest.main()
