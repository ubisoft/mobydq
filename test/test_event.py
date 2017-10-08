"""Unit test for database module."""
import inspect
import os
import sys
import test_utils
import unittest

# Needed to import custom modules from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import database
import event


class TestEventModuleBatch(unittest.TestCase):
    """Class to execute unit tests for database.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.testcaselist = []

    def test_logbatch_batchstart(self):
        """Test log batch function with batch start event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.DatabaseFunction('BatchOwner') as f:
            batchownerlist = f.create(name=testcasename)

        # Start batch
        batch = event.logbatch(testcasename, 'Batch start')

        self.assertEqual(batch.batchOwnerId, batchownerlist[0].id)
        self.assertEqual(batch.statusId, 1)

    def test_logbatch_batchstop(self):
        """Test log batch function with batch stop event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.DatabaseFunction('BatchOwner') as f:
            batchownerlist = f.create(name=testcasename)

        # Start and stop batch
        batch = event.logbatch(testcasename, 'Batch start')
        batch = event.logbatch(testcasename, 'Batch stop')

        self.assertEqual(batch.batchOwnerId, batchownerlist[0].id)
        self.assertEqual(batch.statusId, 2)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for testcasename in self.testcaselist:
            with database.DatabaseFunction('BatchOwner') as f:
                f.delete(name=testcasename)


class TestEventModuleEvent(unittest.TestCase):
    """Class to execute unit tests for database.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.testcaselist = []

    def test_logevent_sessionstart(self):
        """Test log event function with session start event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.DatabaseFunction('BatchOwner') as f:
            batchownerlist = f.create(name=testcasename)

        # Create data quality indicator
        with database.DatabaseFunction('Indicator') as f:
            indicatorlist = f.create(
                name=testcasename,
                description=testcasename,
                indicatorTypeId=1,
                batchOwnerId=batchownerlist[0].id,
                executionOrder=0,
                alertOperator='=',
                alertThreshold='0',
                distributionList=testcasename,
                active=True)

        # Start batch
        batch = event.logbatch(testcasename, 'Batch start')

        # Start session
        sessionstartevent = event.logevent(indicatorlist[0].id, batch.id, 'Session start')

        # Get session
        with database.DatabaseFunction('Session') as f:
            sessionlist = f.read(indicatorId=indicatorlist[0].id, batchId=batch.id)

        self.assertEqual(sessionlist[0].statusId, 1)
        self.assertEqual(sessionstartevent.eventTypeId, 1)
        self.assertEqual(sessionstartevent.sessionId, sessionlist[0].id)

    def test_logevent_sessionstop(self):
        """Test log event function with session stop event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.DatabaseFunction('BatchOwner') as f:
            batchownerlist = f.create(name=testcasename)

        # Create data quality indicator
        with database.DatabaseFunction('Indicator') as f:
            indicatorlist = f.create(
                name=testcasename,
                description=testcasename,
                indicatorTypeId=1,
                batchOwnerId=batchownerlist[0].id,
                executionOrder=0,
                alertOperator='=',
                alertThreshold='0',
                distributionList=testcasename,
                active=True)

        # Start batch
        batch = event.logbatch(testcasename, 'Batch start')

        # Start session
        event.logevent(indicatorlist[0].id, batch.id, 'Session start')

        # Stop session
        sessionstopevent = event.logevent(indicatorlist[0].id, batch.id, 'Session stop')

        # Get session
        with database.DatabaseFunction('Session') as f:
            sessionlist = f.read(indicatorId=indicatorlist[0].id, batchId=batch.id)

        self.assertEqual(sessionlist[0].statusId, 2)
        self.assertEqual(sessionstopevent.eventTypeId, 2)
        self.assertEqual(sessionstopevent.sessionId, sessionlist[0].id)

    def test_logevent_error(self):
        """Test log event function with error event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.DatabaseFunction('BatchOwner') as f:
            batchownerlist = f.create(name=testcasename)

        # Create data quality indicator
        with database.DatabaseFunction('Indicator') as f:
            indicatorlist = f.create(
                name=testcasename,
                description=testcasename,
                indicatorTypeId=1,
                batchOwnerId=batchownerlist[0].id,
                executionOrder=0,
                alertOperator='=',
                alertThreshold='0',
                distributionList=testcasename,
                active=True)

        # Start batch
        batch = event.logbatch(testcasename, 'Batch start')

        # Start session
        event.logevent(indicatorlist[0].id, batch.id, 'Session start')

        # Error
        errorevent = event.logevent(indicatorlist[0].id, batch.id, 'Error')

        # Get session
        with database.DatabaseFunction('Session') as f:
            sessionlist = f.read(indicatorId=indicatorlist[0].id, batchId=batch.id)

        self.assertEqual(sessionlist[0].statusId, 3)
        self.assertEqual(errorevent.eventTypeId, 3)
        self.assertEqual(errorevent.sessionId, sessionlist[0].id)

    def test_logevent_dataset(self):
        """Test log event function with error event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.DatabaseFunction('BatchOwner') as f:
            batchownerlist = f.create(name=testcasename)

        # Create data quality indicator
        with database.DatabaseFunction('Indicator') as f:
            indicatorlist = f.create(
                name=testcasename,
                description=testcasename,
                indicatorTypeId=1,
                batchOwnerId=batchownerlist[0].id,
                executionOrder=0,
                alertOperator='=',
                alertThreshold='0',
                distributionList=testcasename,
                active=True)

        # Start batch
        batch = event.logbatch(testcasename, 'Batch start')

        # Start session
        event.logevent(indicatorlist[0].id, batch.id, 'Session start')

        # Data set
        dataset = {'key': 'value'}
        datasetevent = event.logevent(indicatorlist[0].id, batch.id, 'Data set', dataset)

        # Get session
        with database.DatabaseFunction('Session') as f:
            sessionlist = f.read(indicatorId=indicatorlist[0].id, batchId=batch.id)

        self.assertEqual(sessionlist[0].statusId, 1)
        self.assertEqual(datasetevent.eventTypeId, 4)
        self.assertEqual(datasetevent.sessionId, sessionlist[0].id)
        self.assertEqual(datasetevent.content, dataset)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for testcasename in self.testcaselist:
            # Delete indicator
            with database.DatabaseFunction('Indicator') as f:
                f.delete(name=testcasename)

            # Delete batch owner, batch, session, event
            with database.DatabaseFunction('BatchOwner') as f:
                f.delete(name=testcasename)

if __name__ == '__main__':
    # Test log batch function in event module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventModuleBatch)
    unittest.TextTestRunner(verbosity=2).run(suite)

    # Test log event function in event module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventModuleEvent)
    unittest.TextTestRunner(verbosity=2).run(suite)
