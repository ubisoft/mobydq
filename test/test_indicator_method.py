#!/usr/bin/env python
"""Unit test for indicator_method module."""
from test_utils import get_test_case_name
from api.batch_method import BatchMethod
from api.indicator_method import IndicatorMethod
import api.database.operation as db
import inspect
import os
import unittest


class TestIndicatorMethodModule(unittest.TestCase):
    """Class to execute unit tests for indicator.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_execute_completeness(self):
        """Test execute completeness indicator."""
        test_case_name = get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = db.Operation('BatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = db.Operation('DataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/api/database/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = db.Operation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,  # Completeness
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=1
        )

        # Create indicator paramters
        param = db.Operation('IndicatorParameter')
        param.create(name='Source', value=data_source.name, indicatorId=indicator_record.id)
        param.create(name='Source request', value="select 'status', count(*) from status", indicatorId=indicator_record.id)
        param.create(name='Target', value=data_source.name, indicatorId=indicator_record.id)
        param.create(name='Target request', value="select 'status', count(*)-1 from status", indicatorId=indicator_record.id)
        param.create(name='Dimensions', value="['table_name']", indicatorId=indicator_record.id)
        param.create(name='Measures', value="['nb_records']", indicatorId=indicator_record.id)
        param.create(name='Alert operator', value=">=", indicatorId=indicator_record.id)
        param.create(name='Alert threshold', value="0", indicatorId=indicator_record.id)
        param.create(name='Distribution list', value="['test@test.com']", indicatorId=indicator_record.id)

        # Start batch, execute indicator and stop batch
        batch_record = BatchMethod(batch_owner.id).start()
        IndicatorMethod(indicator_record.id).execute(batch_record.id)
        BatchMethod(batch_owner.id).stop()
        session = db.Operation('Session').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    def test_execute_freshness(self):
        """Test execute freshness indicator."""
        test_case_name = get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = db.Operation('BatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = db.Operation('DataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/api/database/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = db.Operation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=2,  # Freshness
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=1
        )

        # Create indicator paramters
        param = db.Operation('IndicatorParameter')
        param.create(name='Target', value=data_source.name, indicatorId=indicator_record.id)
        param.create(name='Target request', value="select 'status', max(updated_date) from status", indicatorId=indicator_record.id)
        param.create(name='Dimensions', value="['table_name']", indicatorId=indicator_record.id)
        param.create(name='Measures', value="['last_updated_date']", indicatorId=indicator_record.id)
        param.create(name='Alert operator', value=">=", indicatorId=indicator_record.id)
        param.create(name='Alert threshold', value="0", indicatorId=indicator_record.id)
        param.create(name='Distribution list', value="['test@test.com']", indicatorId=indicator_record.id)

        # Start batch, execute indicator and stop batch
        batch_record = BatchMethod(batch_owner.id).start()
        IndicatorMethod(indicator_record.id).execute(batch_record.id)
        BatchMethod(batch_owner.id).stop()
        session = db.Operation('Session').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    def test_execute_latency(self):
        """Test execute latency indicator."""
        test_case_name = get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = db.Operation('BatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = db.Operation('DataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/api/database/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = db.Operation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=3,  # Latency
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=1
        )

        # Create indicator paramters
        param = db.Operation('IndicatorParameter')
        param.create(name='Source', value=data_source.name, indicatorId=indicator_record.id)
        param.create(name='Source request', value="select 'status', max(updated_date) from status", indicatorId=indicator_record.id)
        param.create(name='Target', value=data_source.name, indicatorId=indicator_record.id)
        param.create(name='Target request', value="select 'status', datetime(max(updated_date), '-1 day', '-1 hour') from status", indicatorId=indicator_record.id)
        param.create(name='Dimensions', value="['table_name']", indicatorId=indicator_record.id)
        param.create(name='Measures', value="['last_updated_date']", indicatorId=indicator_record.id)
        param.create(name='Alert operator', value=">=", indicatorId=indicator_record.id)
        param.create(name='Alert threshold', value="0", indicatorId=indicator_record.id)
        param.create(name='Distribution list', value="['test@test.com']", indicatorId=indicator_record.id)

        # Start batch, execute indicator and stop batch
        batch_record = BatchMethod(batch_owner.id).start()
        IndicatorMethod(indicator_record.id).execute(batch_record.id)
        BatchMethod(batch_owner.id).stop()
        session = db.Operation('Session').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    def test_execute_validity(self):
        """Test execute validity indicator."""
        test_case_name = get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = db.Operation('BatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = db.Operation('DataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/api/database/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = db.Operation('Indicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=4,  # Validity
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=1
        )

        # Create indicator paramters
        param = db.Operation('IndicatorParameter')
        param.create(name='Target', value=data_source.name, indicatorId=indicator_record.id)
        param.create(name='Target request', value="select 'status', count(*) from status", indicatorId=indicator_record.id)
        param.create(name='Dimensions', value="['table_name']", indicatorId=indicator_record.id)
        param.create(name='Measures', value="['nb_records']", indicatorId=indicator_record.id)
        param.create(name='Alert operator', value=">=", indicatorId=indicator_record.id)
        param.create(name='Alert threshold', value="0", indicatorId=indicator_record.id)
        param.create(name='Distribution list', value="['test@test.com']", indicatorId=indicator_record.id)

        # Start batch, execute indicator and stop batch
        batch_record = BatchMethod(batch_owner.id).start()
        IndicatorMethod(indicator_record.id).execute(batch_record.id)
        BatchMethod(batch_owner.id).stop()
        session = db.Operation('Session').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            db.Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIndicatorMethodModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
