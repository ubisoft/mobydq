"""Unit test for database module."""
import test_utils
import batch
import database
import unittest


class TestBatchModule(unittest.TestCase):
    """Class to execute unit tests for database.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.testcaselist = []

    def test_logbatch_batchstart(self):
        """Test log batch function with batch start batch."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.Function('BatchOwner') as function:
            batchownerlist = function.create(name=testcasename)

        # Start batch
        batchrecord = batch.logbatch(testcasename, 'Batch start')

        self.assertEqual(batchrecord.batchOwnerId, batchownerlist[0].id)
        self.assertEqual(batchrecord.statusId, 1)

    def test_logbatch_batchstop(self):
        """Test log batch function with batch stop batch."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.Function('BatchOwner') as function:
            batchownerlist = function.create(name=testcasename)

        # Start and stop batch
        batchrecord = batch.logbatch(testcasename, 'Batch start')
        batchrecord = batch.logbatch(testcasename, 'Batch stop')

        self.assertEqual(batchrecord.batchOwnerId, batchownerlist[0].id)
        self.assertEqual(batchrecord.statusId, 2)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for testcasename in self.testcaselist:
            with database.Function('BatchOwner') as function:
                function.delete(name=testcasename)

if __name__ == '__main__':
    # Test log batch function in event module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBatchModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
