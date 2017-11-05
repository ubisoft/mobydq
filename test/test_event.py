#!/usr/bin/env python
"""Unit test for database module."""
import test_utils
import batch
import database
import event
import unittest


class TestEventModule(unittest.TestCase):
    """Class to execute unit tests for event.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_log_event_session_start(self):
        """Test log event function with session start event."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})

        # Create batch owner
        with database.DbOperation('BatchOwner') as op:
            batch_owner = op.create(name=test_case_name)

        # Create data quality indicator
        with database.DbOperation('Indicator') as op:
            indicator = op.create(
                name=test_case_name,
                description=test_case_name,
                indicatorTypeId=1,
                batchOwnerId=batch_owner.id,
                executionOrder=0,
                # alertOperator='=', # This got moved to indicator parameters
                # alertThreshold='0', # This got moved to indicator parameters
                # distributionList=test_case_name, # This got moved to indicator parameters
                active=True)

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Batch start')

        # Start session
        session_start_event = event.log_event(indicator.id, batch_record.id, 'Session start')

        # Get session
        with database.DbOperation('Session') as op:
            session_list = op.read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 1)
        self.assertEqual(session_start_event.eventTypeId, 1)
        self.assertEqual(session_start_event.sessionId, session_list[0].id)

    def test_log_event_session_stop(self):
        """Test log event function with session stop event."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})

        # Create batch owner
        with database.DbOperation('BatchOwner') as op:
            batch_owner = op.create(name=test_case_name)

        # Create data quality indicator
        with database.DbOperation('Indicator') as op:
            indicator = op.create(
                name=test_case_name,
                description=test_case_name,
                indicatorTypeId=1,
                batchOwnerId=batch_owner.id,
                executionOrder=0,
                # alertOperator='=', # This got moved to indicator parameters
                # alertThreshold='0', # This got moved to indicator parameters
                # distributionList=test_case_name, # This got moved to indicator parameters
                active=True)

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Batch start')

        # Start session
        event.log_event(indicator.id, batch_record.id, 'Session start')

        # Stop session
        session_stop_event = event.log_event(indicator.id, batch_record.id, 'Session stop')

        # Get session
        with database.DbOperation('Session') as op:
            session_list = op.read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 2)
        self.assertEqual(session_stop_event.eventTypeId, 2)
        self.assertEqual(session_stop_event.sessionId, session_list[0].id)

    def test_log_event_error(self):
        """Test log event function with error event."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})

        # Create batch owner
        with database.DbOperation('BatchOwner') as op:
            batch_owner = op.create(name=test_case_name)

        # Create data quality indicator
        with database.DbOperation('Indicator') as op:
            indicator = op.create(
                name=test_case_name,
                description=test_case_name,
                indicatorTypeId=1,
                batchOwnerId=batch_owner.id,
                executionOrder=0,
                # alertOperator='=', # This got moved to indicator parameters
                # alertThreshold='0', # This got moved to indicator parameters
                # distributionList=test_case_name, # This got moved to indicator parameters
                active=True)

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Batch start')

        # Start session
        event.log_event(indicator.id, batch_record.id, 'Session start')

        # Error
        error_event = event.log_event(indicator.id, batch_record.id, 'Error')

        # Get session
        with database.DbOperation('Session') as op:
            session_list = op.read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 3)
        self.assertEqual(error_event.eventTypeId, 3)
        self.assertEqual(error_event.sessionId, session_list[0].id)

    def test_log_event_data_set(self):
        """Test log event function with data_set event."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})

        # Create batch owner
        with database.DbOperation('BatchOwner') as op:
            batch_owner = op.create(name=test_case_name)

        # Create data quality indicator
        with database.DbOperation('Indicator') as op:
            indicator = op.create(
                name=test_case_name,
                description=test_case_name,
                indicatorTypeId=1,
                batchOwnerId=batch_owner.id,
                executionOrder=0,
                # alertOperator='=', # This got moved to indicator parameters
                # alertThreshold='0', # This got moved to indicator parameters
                # distributionList=test_case_name, # This got moved to indicator parameters
                active=True)

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Batch start')

        # Start session
        event.log_event(indicator.id, batch_record.id, 'Session start')

        # Data set
        data_set = {'key': 'value'}
        data_set_event = event.log_event(indicator.id, batch_record.id, 'Data set', data_set)

        # Get session
        with database.DbOperation('Session') as op:
            session_list = op.read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 1)
        self.assertEqual(data_set_event.eventTypeId, 4)
        self.assertEqual(data_set_event.sessionId, session_list[0].id)
        self.assertEqual(data_set_event.content, data_set)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            # Delete indicator
            with database.DbOperation('Indicator') as op:
                op.delete(name=test_case['test_case'])

            # Delete batch owner, batch, session, event
            with database.DbOperation('BatchOwner') as op:
                op.delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test log event function in event module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
