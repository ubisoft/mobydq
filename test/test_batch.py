"""Unit test for database module."""
import test_utils
import batch
import database
import unittest


class TestBatchModule(unittest.TestCase):
    """Class to execute unit tests for batch.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.testcaselist = []

    def test_logbatch_batchstart(self):
        """Test log batch function with batch start batch."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'BatchOwner', 'testcase': testcasename})

        # Create batch owner
        with database.DbOperation('BatchOwner') as op:
            batchowner = op.create(name=testcasename)

        # Start batch
        batchrecord = batch.logbatch(batchowner.id, 'Batch start')

        self.assertEqual(batchrecord.batchOwnerId, batchowner.id)
        self.assertEqual(batchrecord.statusId, 1)

    def test_logbatch_batchstop(self):
        """Test log batch function with batch stop batch."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'BatchOwner', 'testcase': testcasename})

        # Create batch owner
        with database.DbOperation('BatchOwner') as op:
            batchowner = op.create(name=testcasename)

        # Start and stop batch
        batchrecord = batch.logbatch(batchowner.id, 'Batch start')
        batchrecord = batch.logbatch(batchowner.id, 'Batch stop')

        self.assertEqual(batchrecord.batchOwnerId, batchowner.id)
        self.assertEqual(batchrecord.statusId, 2)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for testcase in self.testcaselist:
            with database.DbOperation(testcase['class']) as op:
                op.delete(name=testcase['testcase'])


if __name__ == '__main__':
    # Test log batch function in batch module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBatchModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
