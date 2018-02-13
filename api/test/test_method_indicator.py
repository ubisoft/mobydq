#!/usr/bin/env python
"""Unit test for method_indicator module."""
from api.database.operation import Operation
from api.method_batch import MethodBatch
from api.method_indicator import MethodIndicator
from test import test_utils
import inspect
import os
import unittest


class TestMethodIndicatorModule(unittest.TestCase):
    """Class to execute unit tests for indicator.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_execute_completeness(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelIndicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelDataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelBatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = Operation('ModelDataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/database/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = Operation('ModelIndicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=1,  # Completeness
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=1
        )

        # Create indicator paramters
        param = Operation('ModelIndicatorParameter')
        param.create(parameterTypeId=1, value=">=", indicatorId=indicator_record.id)  # Alert operator
        param.create(parameterTypeId=2, value="0", indicatorId=indicator_record.id)  # Alert threshold
        param.create(parameterTypeId=3, value="['nb_records']", indicatorId=indicator_record.id)  # Measures
        param.create(parameterTypeId=4, value="['table_name']", indicatorId=indicator_record.id)  # Dimensions
        param.create(parameterTypeId=5, value=data_source.name, indicatorId=indicator_record.id)  # Target
        param.create(parameterTypeId=6, value="select 'status', count(*)-1 from status", indicatorId=indicator_record.id)  # Target request
        param.create(parameterTypeId=7, value=data_source.name, indicatorId=indicator_record.id)  # Source
        param.create(parameterTypeId=8, value="select 'status', count(*) from status", indicatorId=indicator_record.id)  # Source request
        param.create(parameterTypeId=9, value="['test@test.com']", indicatorId=indicator_record.id)  # Distribution list

        # Start batch, execute indicator and stop batch
        batch_record = MethodBatch(batch_owner.id).start()
        MethodIndicator(indicator_record.id).execute(batch_record.id)
        MethodBatch(batch_owner.id).stop(batch_record.id)
        session = Operation('ModelSession').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    def test_execute_freshness(self):
        """Test execute freshness indicator."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelIndicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelDataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelBatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = Operation('ModelDataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/database/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = Operation('ModelIndicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=2,  # Freshness
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=1
        )

        # Create indicator paramters
        param = Operation('ModelIndicatorParameter')
        param.create(parameterTypeId=1, value=">=", indicatorId=indicator_record.id)  # Alert operator
        param.create(parameterTypeId=2, value="0", indicatorId=indicator_record.id)  # Alert threshold
        param.create(parameterTypeId=3, value="['last_updated_date']", indicatorId=indicator_record.id)  # Measures
        param.create(parameterTypeId=4, value="['table_name']", indicatorId=indicator_record.id)  # Dimensions
        param.create(parameterTypeId=5, value=data_source.name, indicatorId=indicator_record.id)  # Target
        param.create(parameterTypeId=6, value="select 'status', max(updated_date) from status", indicatorId=indicator_record.id)  # Target request
        param.create(parameterTypeId=9, value="['test@test.com']", indicatorId=indicator_record.id)  # Distribution list

        # Start batch, execute indicator and stop batch
        batch_record = MethodBatch(batch_owner.id).start()
        MethodIndicator(indicator_record.id).execute(batch_record.id)
        MethodBatch(batch_owner.id).stop(batch_record.id)
        session = Operation('ModelSession').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    def test_execute_latency(self):
        """Test execute latency indicator."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelIndicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelDataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelBatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = Operation('ModelDataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/database/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = Operation('ModelIndicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=3,  # Latency
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=1
        )

        # Create indicator paramters
        param = Operation('ModelIndicatorParameter')
        param.create(parameterTypeId=1, value=">=", indicatorId=indicator_record.id)  # Alert operator
        param.create(parameterTypeId=2, value="0", indicatorId=indicator_record.id)  # Alert threshold
        param.create(parameterTypeId=3, value="['last_updated_date']", indicatorId=indicator_record.id)  # Measures
        param.create(parameterTypeId=4, value="['table_name']", indicatorId=indicator_record.id)  # Dimensions
        param.create(parameterTypeId=5, value=data_source.name, indicatorId=indicator_record.id)  # Target
        param.create(parameterTypeId=6, value="select 'status', datetime(max(updated_date), '-1 day', '-1 hour') from status", indicatorId=indicator_record.id)  # Target request
        param.create(parameterTypeId=7, value=data_source.name, indicatorId=indicator_record.id)  # Source
        param.create(parameterTypeId=8, value="select 'status', max(updated_date) from status", indicatorId=indicator_record.id)  # Source request
        param.create(parameterTypeId=9, value="['test@test.com']", indicatorId=indicator_record.id)  # Distribution list

        # Start batch, execute indicator and stop batch
        batch_record = MethodBatch(batch_owner.id).start()
        MethodIndicator(indicator_record.id).execute(batch_record.id)
        MethodBatch(batch_owner.id).stop(batch_record.id)
        session = Operation('ModelSession').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    def test_execute_validity(self):
        """Test execute validity indicator."""
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelIndicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelDataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'ModelBatchOwner', 'test_case': test_case_name})

        # Create batch owner
        batch_owner = Operation('ModelBatchOwner').create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        data_source = Operation('ModelDataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/database/data_quality.db',
            login='',
            password=''
        )

        # Create indicator
        indicator_record = Operation('ModelIndicator').create(
            name=test_case_name,
            description=test_case_name,
            indicatorTypeId=4,  # Validity
            batchOwnerId=batch_owner.id,
            executionOrder=0,
            active=1
        )

        # Create indicator paramters
        param = Operation('ModelIndicatorParameter')
        param.create(parameterTypeId=1, value=">=", indicatorId=indicator_record.id)  # Alert operator
        param.create(parameterTypeId=2, value="0", indicatorId=indicator_record.id)  # Alert threshold
        param.create(parameterTypeId=3, value="['nb_records']", indicatorId=indicator_record.id)  # Measures
        param.create(parameterTypeId=4, value="['table_name']", indicatorId=indicator_record.id)  # Dimensions
        param.create(parameterTypeId=5, value=data_source.name, indicatorId=indicator_record.id)  # Target
        param.create(parameterTypeId=6, value="select 'status', count(*) from status", indicatorId=indicator_record.id)  # Target request
        param.create(parameterTypeId=9, value="['test@test.com']", indicatorId=indicator_record.id)  # Distribution list

        # Start batch, execute indicator and stop batch
        batch_record = MethodBatch(batch_owner.id).start()
        MethodIndicator(indicator_record.id).execute(batch_record.id)
        MethodBatch(batch_owner.id).stop(batch_record.id)
        session = Operation('ModelSession').read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMethodIndicatorModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
