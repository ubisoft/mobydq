#!/usr/bin/env python
"""Unit test for method_data_source module."""
from api.database.operation import Operation
from api.method_data_source import MethodDataSource
from test import test_utils
import inspect
import os
import unittest


class TestMethodDataSourceModule(unittest.TestCase):
    """Class to execute unit tests for batch.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.test_case_list = []

    def test_get_database_connection(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelDataSource', 'test_case': test_case_name})

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        Operation('ModelDataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/database/data_quality.db',
            login='',
            password=''
        )

        # Get data source connection and execute dummy query
        connection = MethodDataSource(test_case_name).get_database_connection()
        cursor = connection.cursor()
        cursor.execute("select 'Hello World' as text")

        for row in cursor:
            self.assertEqual(row[0], 'Hello World')

    def test_get_data_frame(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'ModelDataSource', 'test_case': test_case_name})

        # Create data source
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_directory = os.path.dirname(current_directory)
        Operation('ModelDataSource').create(
            name=test_case_name,
            dataSourceTypeId=6,  # SQLite
            connectionString=parent_directory + '/database/data_quality.db',
            login='',
            password=''
        )

        # Get data frame
        request = "select 'status', count(*) as nb_records from status"
        data_frame = MethodDataSource(test_case_name).get_data_frame(request)

        for row in data_frame.index:
            self.assertGreaterEqual(data_frame.loc[row, 'nb_records'], 0)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMethodDataSourceModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
