#!/usr/bin/env python
"""Unit test for database module."""
import test_utils
from api.database.operation import Operation
import unittest


class TestDatabaseModule(unittest.TestCase):
    """Class to execute unit tests for database.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_create_batch_owner(self):
        """Test create function."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        batch_owner = Operation('BatchOwner').create(name=test_case_name)

        self.assertEqual(batch_owner.name, test_case_name)

    def test_read_batch_owner(self):
        """Test read function."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        Operation('BatchOwner').create(name=test_case_name)

        batch_owner_list = Operation('BatchOwner').read(name=test_case_name)

        self.assertEqual(batch_owner_list[0].name, test_case_name)

    def test_update_batch_owner(self):
        """Test update function."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        batch_owner = Operation('BatchOwner').create(name=test_case_name)

        test_case_name_new = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name_new})

        batch_owner = Operation('BatchOwner').update(id=batch_owner.id, name=test_case_name_new)

        self.assertEqual(batch_owner.name, test_case_name_new)

    def test_delete_batch_owner(self):
        """Test delete function."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        batch_owner = Operation('BatchOwner').create(name=test_case_name)

        Operation('BatchOwner').delete(id=batch_owner.id)

        batch_owner_list = Operation('BatchOwner').read(name=test_case_name)

        self.assertEqual(batch_owner_list, [])

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test database functions in database module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
