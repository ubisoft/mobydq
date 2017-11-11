#!/usr/bin/env python
"""Unit test for indicator module."""
import test_utils
import inspect
import os
import batch
import indicator
import database
import unittest


class TestIndicatorModule(unittest.TestCase):
    """Class to execute unit tests for indicator.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_execute_validity(self):
        """Test execute indicator for validity module."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        with database.DbOperation('BatchOwner') as op:
            batch_owner = op.create(name=test_case_name)

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        print(parent_directory)
        with database.DbOperation('DataSource') as op:
            data_source = op.create(
                name=test_case_name,
                dataSourceTypeId=6,  # SQLite
                connectionString=parent_directory + '/data_quality.db',
                login='',
                password='')

        # Create indicator
        with database.DbOperation('Indicator') as op:
            indicator_record = op.create(
                name=test_case_name,
                description=test_case_name,
                indicatorTypeId=4,
                batchOwnerId=batch_owner.id,
                executionOrder=0,
                # alertOperator='=', # This got moved to indicator parameters
                # alertThreshold='1', # This got moved to indicator parameters
                # distributionList='test@test.com', # This got moved to indicator parameters
                active=1)

        # Create indicator paramters
        with database.DbOperation('IndicatorParameter') as op:
            op.create(name='Target', value=data_source.name, indicatorId=indicator_record.id)
            op.create(name='Target request', value="select 'status', count(*) from status", indicatorId=indicator_record.id)
            op.create(name='Dimensions', value="['table_name']", indicatorId=indicator_record.id)
            op.create(name='Measures', value="['nb_records']", indicatorId=indicator_record.id)
            op.create(name='Alert operator', value=">=", indicatorId=indicator_record.id)
            op.create(name='Alert threshold', value="0", indicatorId=indicator_record.id)
            op.create(name='Distribution list', value="['test@test.com']", indicatorId=indicator_record.id)

        # Start batch
        batch_record = batch.log_batch(batch_owner.id, 'Start')

        # Execute indicator
        indicator.execute(indicator_record.id, batch_record.id)

        # Stop batch
        batch_record = batch.log_batch(batch_owner.id, 'Stop')

        # Get session status
        with database.DbOperation('Session') as op:
            session = op.read(indicatorId=indicator_record.id, batchId=batch_record.id)

        self.assertEqual(session[0].statusId, 2)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            with database.DbOperation(test_case['class']) as op:
                op.delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test execute function in indicator module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIndicatorModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
