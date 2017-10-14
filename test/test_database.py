"""Unit test for database module."""
import test_utils
import database
import unittest


class TestDatabaseModule(unittest.TestCase):
    """Class to execute unit tests for database.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.testcaselist = []

    def test_create_batchowner(self):
        """Test create function."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        with database.Function('BatchOwner') as f:
            batchownerlist = f.create(name=testcasename)

        self.assertEqual(batchownerlist[0].name, testcasename)

    def test_read_batchowner(self):
        """Test read function."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        with database.Function('BatchOwner') as f:
            f.create(name=testcasename)

        with database.Function('BatchOwner') as f:
            batchownerlist = f.read(name=testcasename)

        self.assertEqual(batchownerlist[0].name, testcasename)

    def test_update_batchowner(self):
        """Test update function."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        with database.Function('BatchOwner') as f:
            batchownerlist = f.create(name=testcasename)

        testcasenamenew = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasenamenew)

        with database.Function('BatchOwner') as f:
            f.update(id=batchownerlist[0].id, name=testcasenamenew)

        with database.Function('BatchOwner') as f:
            batchownerlist = f.read(name=testcasenamenew)

        self.assertEqual(batchownerlist[0].name, testcasenamenew)

    def test_delete_batchowner(self):
        """Test delete function."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        with database.Function('BatchOwner') as f:
            batchownerlist = f.create(name=testcasename)

        with database.Function('BatchOwner') as f:
            f.delete(id=batchownerlist[0].id)

        with database.Function('BatchOwner') as f:
            batchownerlist = f.read(name=testcasename)

        self.assertEqual(batchownerlist, [])

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for testcasename in self.testcaselist:
            with database.Function('BatchOwner') as f:
                f.delete(name=testcasename)

if __name__ == '__main__':
    # Test database functions in database module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
