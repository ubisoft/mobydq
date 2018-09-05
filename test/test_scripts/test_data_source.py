from datetime import datetime
from scripts.init.data_source import DataSource
from scripts.init import utils
import time
import unittest


class TestDataSource(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    @staticmethod
    def get_test_case_name():
        """Generate unique name for unit test case."""
        time.sleep(1)
        test_case_name = 'test {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return test_case_name

    def test_get_connection_mysql(self):
        pass

    def test_get_connection_postgresql(self):
        pass

    def test_get_connection_sql_server(self):
        pass

    def test_get_connection_sqlite(self):
        pass

    def test_get_connection_teradata(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass


if __name__ == '__main__':
    unittest.main()
