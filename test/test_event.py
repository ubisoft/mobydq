#!/usr/bin/env python
"""Unit test for database module."""
from api.database import Operation
import test_utils
import batch
import event
import unittest


class TestEventModule(unittest.TestCase):
    """Class to execute unit tests for event.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_log_event_session_start(self):
        """Test log event function with start event."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('BatchOwner').create(name=test_case_name)

        # Create data quality indicator
        indicator = Operation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=True
        )

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Start')

        # Start session
        session_start_event = event.log_event(indicator.id, batch_record.id, 'Start')

        # Get session
        session_list = Operation('Session').read(
            indicatorId=indicator.id, batchId=batch_record.id
        )

        self.assertEqual(session_list[0].statusId, 1)
        self.assertEqual(session_start_event.eventTypeId, 1)
        self.assertEqual(session_start_event.sessionId, session_list[0].id)

    def test_log_event_session_stop(self):
        """Test log event function with stop event."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('BatchOwner').create(name=test_case_name)

        # Create data quality indicator
        indicator = Operation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=True
        )

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Start')

        # Start session
        event.log_event(indicator.id, batch_record.id, 'Start')

        # Stop session
        session_stop_event = event.log_event(indicator.id, batch_record.id, 'Stop')

        # Get session
        session_list = Operation('Session').read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 2)
        self.assertEqual(session_stop_event.eventTypeId, 2)
        self.assertEqual(session_stop_event.sessionId, session_list[0].id)

    def test_log_event_error(self):
        """Test log event function with error event."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('BatchOwner').create(name=test_case_name)

        # Create data quality indicator
        indicator = Operation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=True
        )

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Start')

        # Start session
        event.log_event(indicator.id, batch_record.id, 'Start')

        # Error
        error_event = event.log_event(indicator.id, batch_record.id, 'Error')

        # Get session
        session_list = Operation('Session').read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 3)
        self.assertEqual(error_event.eventTypeId, 3)
        self.assertEqual(error_event.sessionId, session_list[0].id)

    def test_log_event_data_set(self):
        """Test log event function with data_set event."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('BatchOwner').create(name=test_case_name)

        # Create data quality indicator
        indicator = Operation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=True
        )

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Start')

        # Start session
        event.log_event(indicator.id, batch_record.id, 'Start')

        # Data set
        data_set = {'key': 'value'}
        data_set_event = event.log_event(indicator.id, batch_record.id, 'Data set', data_set)

        # Get session
        session_list = Operation('Session').read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 1)
        self.assertEqual(data_set_event.eventTypeId, 4)
        self.assertEqual(data_set_event.sessionId, session_list[0].id)
        self.assertEqual(data_set_event.content, data_set)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test log event function in event module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
