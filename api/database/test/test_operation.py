#!/usr/bin/env python
"""Unit test for database operation module."""
from api.database.operation import Operation
from test import test_utils
import unittest


class TestOperationModule(unittest.TestCase):
    """Class to execute unit tests for operation.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_create(self):
        """Test create function."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        self.assertEqual(batch_owner.name, test_case_name)

    def test_read(self):
        """Test read function."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        Operation('ModelBatchOwner').create(name=test_case_name)

        batch_owner_list = Operation('ModelBatchOwner').read(name=test_case_name)

        self.assertEqual(batch_owner_list[0].name, test_case_name)

    def test_update(self):
        """Test update function."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        test_case_name_new = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name_new})

        batch_owner = Operation('ModelBatchOwner').update(id=batch_owner.id, name=test_case_name_new)

        self.assertEqual(batch_owner.name, test_case_name_new)

    def test_delete(self):
        """Test delete function."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        Operation('ModelBatchOwner').delete(id=batch_owner.id)

        batch_owner_list = Operation('ModelBatchOwner').read(name=test_case_name)

        self.assertEqual(batch_owner_list, [])

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOperationModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
