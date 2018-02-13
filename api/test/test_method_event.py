#!/usr/bin/env python
"""Unit test for method_event module."""
from api.database.operation import Operation
from api.method_batch import MethodBatch
from api.method_event import MethodEvent
from test import test_utils
import unittest


class TestMethodEventModule(unittest.TestCase):
    """Class to execute unit tests for event.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_log_event_start(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelIndicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelBatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Create data quality indicator
        indicator = Operation('ModelIndicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=True
        )

        # Start batch and session
        batch_record = MethodBatch(batch_owner.id).start()
        start_event = MethodEvent('Start').log_event(indicator.id, batch_record.id)
        session_list = Operation('ModelSession').read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 1)
        self.assertEqual(start_event.eventTypeId, 1)
        self.assertEqual(start_event.sessionId, session_list[0].id)

    def test_log_event_stop(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelIndicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelBatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Create data quality indicator
        indicator = Operation('ModelIndicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=True
        )

        # Start batch, session and fail session
        batch_record = MethodBatch(batch_owner.id).start()
        MethodEvent('Start').log_event(indicator.id, batch_record.id)
        stop_event = MethodEvent('Stop').log_event(indicator.id, batch_record.id)
        session_list = Operation('ModelSession').read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 2)
        self.assertEqual(stop_event.eventTypeId, 2)
        self.assertEqual(stop_event.sessionId, session_list[0].id)

    def test_log_event_error(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelIndicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelBatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Create data quality indicator
        indicator = Operation('ModelIndicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=True
        )

        # Start batch, session and stop session
        batch_record = MethodBatch(batch_owner.id).start()
        MethodEvent('Start').log_event(indicator.id, batch_record.id)
        error_event = MethodEvent('Error').log_event(indicator.id, batch_record.id)
        session_list = Operation('ModelSession').read(indicatorId=indicator.id, batchId=batch_record.id)

        self.assertEqual(session_list[0].statusId, 3)
        self.assertEqual(error_event.eventTypeId, 3)
        self.assertEqual(error_event.sessionId, session_list[0].id)

    def test_log_event_data_set(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelIndicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelBatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Create data quality indicator
        indicator = Operation('ModelIndicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=True
        )

        # Start batch, session and stop session
        batch_record = MethodBatch(batch_owner.id).start()
        MethodEvent('Start').log_event(indicator.id, batch_record.id)
        data_set = {'key': 'value'}
        data_set_event = MethodEvent('Data set').log_event(indicator.id, batch_record.id, data_set)
        session_list = Operation('ModelSession').read(indicatorId=indicator.id, batchId=batch_record.id)

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
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMethodEventModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
