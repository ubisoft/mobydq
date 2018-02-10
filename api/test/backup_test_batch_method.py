#!/usr/bin/env python
"""Unit test for batch_method module."""
from api.database.operation import Operation
from api.batch_method import BatchMethod
from test import test_utils
import unittest


class TestBatchMethodModule(unittest.TestCase):
    """Class to execute unit tests for batch.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_batch_start(self):
        """Test batch start function."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Start batch
        batch_record = BatchMethod(batch_owner.id).start()

        self.assertEqual(batch_record.batchOwnerId, batch_owner.id)
        self.assertEqual(batch_record.statusId, 1)

    def test_batch_stop(self):
        """Test batch stop function."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Start and stop batch
        batch_record = BatchMethod(batch_owner.id).start()
        batch_record = BatchMethod(batch_owner.id).stop(batch_record.id)

        self.assertEqual(batch_record.batchOwnerId, batch_owner.id)
        self.assertEqual(batch_record.statusId, 2)

    def test_batch_fail(self):
        """Test log batch function with error event."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Start and fail batch
        batch_record = BatchMethod(batch_owner.id).start()
        batch_record = BatchMethod(batch_owner.id).fail(batch_record.id)

        self.assertEqual(batch_record.batchOwnerId, batch_owner.id)
        self.assertEqual(batch_record.statusId, 3)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBatchMethodModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
