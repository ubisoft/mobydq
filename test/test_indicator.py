#!/usr/bin/env python
"""Unit test for indicator module."""
import test_utils
import batch
import indicator
import database
import unittest


class TestIndicatorModule(unittest.TestCase):
    """Class to execute unit tests for indicator.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.testcaselist = []

    def test_execute_validity(self):
        """Test execute indicator function with validity indicator type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'BatchOwner', 'testcase': testcasename})
        self.testcaselist.append({'class': 'Indicator', 'testcase': testcasename})

        # Create batch owner
        with database.DbOperation('BatchOwner') as op:
            batchowner = op.create(name=testcasename)

        # Create indicator
        with database.DbOperation('Indicator') as op:
            indicatorrecord = op.create(
                name=testcasename,
                description=testcasename,
                indicatorTypeId=4,
                batchOwnerId=batchowner.id,
                executionOrder=0,
                alertOperator='=',
                alertThreshold='1',
                distributionList='test@test.com',
                active=1)

        # Start batch
        batchrecord = batch.logbatch(batchowner.id, 'Batch start')

        # Execute indicator
        indicator.execute(indicatorrecord.id, batchrecord.id)

        # Stop batch
        batchrecord = batch.logbatch(batchowner.id, 'Batch stop')

        # Get session status
        with database.DbOperation('Session') as op:
            session = op.read(indicatorId=indicatorrecord.id, batchId=batchrecord.id)

        self.assertEqual(session[0].statusId, 2)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for testcase in self.testcaselist:
            # Delete indicator
            with database.DbOperation('Indicator') as op:
                op.delete(name=testcase['testcase'])

            # Delete batch owner, batch, session, event
            with database.DbOperation('BatchOwner') as op:
                op.delete(name=testcase['testcase'])


if __name__ == '__main__':
    # Test execute function in indicator module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIndicatorModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
