from datetime import datetime
from scripts.data_source import DataSource
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

    def test_get_connection_sql_server(self):
        # Set connection parameters
        data_source_type_id = 4
        connection_string = 'driver={FreeTDS};server=db-sql-server;port=1433;database=star_wars;tds_version=8.0;'
        login = 'sa'
        password = '1234-abcd'

        # Connect to test database
        data_source = DataSource()
        connection = data_source.get_connection(data_source_type_id, connection_string, login, password)
        cursor = connection.cursor()
        result = cursor.execute("SELECT name FROM star_wars.dbo.planet WHERE name='Tatooine';").fetchone()
        result = result[0]
        cursor.close()
        connection.close()

        # Assert query result
        self.assertEqual(result, 'Tatooine')

    def test_get_connection_mysql(self):
        # Set connection parameters
        data_source_type_id = 5
        connection_string = 'driver={MySQL Unicode};server=db-mysql;port=3306;database=star_wars;'
        login = 'root'
        password = '1234'

        # Connect to test database
        data_source = DataSource()
        connection = data_source.get_connection(data_source_type_id, connection_string, login, password)
        cursor = connection.cursor()
        result = cursor.execute("SELECT name FROM star_wars.planet WHERE name='Tatooine';").fetchone()
        result = result[0]
        cursor.close()
        connection.close()

        # Assert query result
        self.assertEqual(result, 'Tatooine')

        # Assert query result
        self.assertEqual(result, 'Tatooine')

    def test_get_connection_postgresql(self):
        # Set connection parameters
        data_source_type_id = 7
        connection_string = 'driver={PostgreSQL Unicode};server=db-postgresql;port=5432;database=star_wars;'
        login = 'postgres'
        password = '1234'

        # Connect to test database
        data_source = DataSource()
        connection = data_source.get_connection(data_source_type_id, connection_string, login, password)
        cursor = connection.cursor()
        result = cursor.execute("SELECT name FROM public.planet WHERE name='Tatooine';").fetchone()
        result = result[0]
        cursor.close()
        connection.close()

        # Assert query result
        self.assertEqual(result, 'Tatooine')

    def test_get_connection_sqlite(self):
        # Set connection parameters
        data_source_type_id = 8
        connection_string = './star_wars.db'

        # Connect to test database
        data_source = DataSource()
        connection = data_source.get_connection(data_source_type_id, connection_string)
        cursor = connection.cursor()
        result = cursor.execute("SELECT name FROM planet WHERE name='Tatooine';").fetchone()
        result = result[0]
        cursor.close()
        connection.close()

        # Assert query result
        self.assertEqual(result, 'Tatooine')

    def test_get_connection_teradata(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass


if __name__ == '__main__':
    unittest.main()
