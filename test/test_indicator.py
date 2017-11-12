#!/usr/bin/env python
"""Unit test for indicator module."""
import test_utils
import inspect
import os
import batch
import indicator
from database import DbOperation
import unittest


class TestIndicatorModule(unittest.TestCase):
    """Class to execute unit tests for indicator.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_execute_completeness(self):
        """Test execute completeness indicator."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = DbOperation('BatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = DbOperation('DataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = DbOperation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,  # Completeness
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            # alertOperator='=', # This got moved to indicator parameters
            # alertThreshold='1', # This got moved to indicator parameters
            # distributionList='test@test.com', # This got moved to indicator parameters
            active=1
        )

        # Create indicator paramters
        db_op = DbOperation('IndicatorParameter')
        with db_op.open_session() as session:
            db_op._create(session, name='Source', value=data_source.name, indicatorId=indicator_record.id)
            db_op._create(session, name='Source request', value="select 'status', count(*) from status",
                          indicatorId=indicator_record.id)
            db_op._create(session, name='Target', value=data_source.name, indicatorId=indicator_record.id)
            db_op._create(session, name='Target request', value="select 'status', count(*)-1 from status",
                          indicatorId=indicator_record.id)
            db_op._create(session, name='Dimensions', value="['table_name']", indicatorId=indicator_record.id)
            db_op._create(session, name='Measures', value="['nb_records']", indicatorId=indicator_record.id)
            db_op._create(session, name='Alert operator', value=">=", indicatorId=indicator_record.id)
            db_op._create(session, name='Alert threshold', value="0", indicatorId=indicator_record.id)
            db_op._create(session, name='Distribution list', value="['test@test.com']", indicatorId=indicator_record.id)

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Start')

        # Execute indicator
        indicator.execute(indicator_record.id, batch_record.id)

        # Stop batch
        batch_record = batch.log_batch(batch_owner.id, 'Stop')

        # Get session status
        session = DbOperation('Session').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    def test_execute_freshness(self):
        """Test execute freshness indicator."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = DbOperation('BatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = DbOperation('DataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = DbOperation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=2,  # Freshness
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            # alertOperator='=', # This got moved to indicator parameters
            # alertThreshold='1', # This got moved to indicator parameters
            # distributionList='test@test.com', # This got moved to indicator parameters
            active=1
        )

        # Create indicator paramters
        db_op = DbOperation('IndicatorParameter')
        with db_op.open_session() as session:
            db_op._create(session, name='Target', value=data_source.name, indicatorId=indicator_record.id)
            db_op._create(session, name='Target request', value="select 'status', max(updated_date) from status",
                          indicatorId=indicator_record.id)
            db_op._create(session, name='Dimensions', value="['table_name']", indicatorId=indicator_record.id)
            db_op._create(session, name='Measures', value="['last_updated_date']", indicatorId=indicator_record.id)
            db_op._create(session, name='Alert operator', value=">=", indicatorId=indicator_record.id)
            db_op._create(session, name='Alert threshold', value="0", indicatorId=indicator_record.id)
            db_op._create(session, name='Distribution list', value="['test@test.com']", indicatorId=indicator_record.id)

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Start')

        # Execute indicator
        indicator.execute(indicator_record.id, batch_record.id)

        # Stop batch
        batch_record = batch.log_batch(batch_owner.id, 'Stop')

        # Get session status
        session = DbOperation('Session').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    def test_execute_latency(self):
        """Test execute latency indicator."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = DbOperation('BatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = DbOperation('DataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = DbOperation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=3,  # Latency
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            # alertOperator='=', # This got moved to indicator parameters
            # alertThreshold='1', # This got moved to indicator parameters
            # distributionList='test@test.com', # This got moved to indicator parameters
            active=1
        )

        # Create indicator paramters
        db_op = DbOperation('IndicatorParameter')
        with db_op.open_session() as session:
            db_op._create(session, name='Source', value=data_source.name, indicatorId=indicator_record.id)
            db_op._create(session, name='Source request', value="select 'status', max(updated_date) from status",
                          indicatorId=indicator_record.id)
            db_op._create(session, name='Target', value=data_source.name, indicatorId=indicator_record.id)
            db_op._create(session, name='Target request',
                          value="select 'status', datetime(max(updated_date), '-1 day', '-1 hour') from status",
                          indicatorId=indicator_record.id)
            db_op._create(session, name='Dimensions', value="['table_name']", indicatorId=indicator_record.id)
            db_op._create(session, name='Measures', value="['last_updated_date']", indicatorId=indicator_record.id)
            db_op._create(session, name='Alert operator', value=">=", indicatorId=indicator_record.id)
            db_op._create(session, name='Alert threshold', value="0", indicatorId=indicator_record.id)
            db_op._create(session, name='Distribution list', value="['test@test.com']", indicatorId=indicator_record.id)

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Start')

        # Execute indicator
        indicator.execute(indicator_record.id, batch_record.id)

        # Stop batch
        batch_record = batch.log_batch(batch_owner.id, 'Stop')

        # Get session status
        session = DbOperation('Session').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    def test_execute_validity(self):
        """Test execute validity indicator."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = DbOperation('BatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = DbOperation('DataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = DbOperation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=4,  # Validity
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            # alertOperator='=', # This got moved to indicator parameters
            # alertThreshold='1', # This got moved to indicator parameters
            # distributionList='test@test.com', # This got moved to indicator parameters
            active=1
        )

        # Create indicator paramters
        db_op = DbOperation('IndicatorParameter')
        with db_op.open_session() as session:
            db_op._create(session, name='Target', value=data_source.name, indicatorId=indicator_record.id)
            db_op._create(session, name='Target request', value="select 'status', count(*) from status",
                          indicatorId=indicator_record.id)
            db_op._create(session, name='Dimensions', value="['table_name']", indicatorId=indicator_record.id)
            db_op._create(session, name='Measures', value="['nb_records']", indicatorId=indicator_record.id)
            db_op._create(session, name='Alert operator', value=">=", indicatorId=indicator_record.id)
            db_op._create(session, name='Alert threshold', value="0", indicatorId=indicator_record.id)
            db_op._create(session, name='Distribution list', value="['test@test.com']", indicatorId=indicator_record.id)

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Start')

        # Execute indicator
        indicator.execute(indicator_record.id, batch_record.id)

        # Stop batch
        batch_record = batch.log_batch(batch_owner.id, 'Stop')

        # Get session status
        session = DbOperation('Session').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            DbOperation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test execute function in indicator module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIndicatorModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
