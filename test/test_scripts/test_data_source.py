"""Unit tests for module /scripts/init/data_source.py."""
import unittest
from scripts.data_source import DataSource
from scripts.constants import DataSourceType


class TestDataSource(unittest.TestCase):
    """Unit tests for class DataSource."""

    def test_get_connection_mariadb(self):
        """Unit tests for method get_connection for MariaDB database."""

        # Set connection parameters
        data_source_type_id = DataSourceType.MARIADB_ID
        connection_string = 'driver={MariaDB Unicode};server=db-mariadb;port=3306;Database=star_wars;'
        login = 'root'
        password = '1234'

        # Connect to test Database
        data_source = DataSource()
        connection = data_source.get_connection(data_source_type_id, connection_string, login, password)
        cursor = connection.cursor()
        result = cursor.execute("SELECT name FROM star_wars.planet WHERE name='Tatooine';").fetchone()
        result = result[0]
        cursor.close()
        connection.close()

        # Assert query result
        self.assertEqual(result, 'Tatooine')

    def test_get_connection_sql_server(self):
        """Unit tests for method get_connection for Microsoft SQL Server database."""

        # Set connection parameters
        data_source_type_id = DataSourceType.MSSQL_ID
        connection_string = 'driver={FreeTDS};server=db-sql-server;port=1433;Database=star_wars;tds_version=8.0;'
        login = 'sa'
        password = '1234-abcd'

        # Connect to test Database
        data_source = DataSource()
        connection = data_source.get_connection(data_source_type_id, connection_string, login, password)
        cursor = connection.cursor()
        result = cursor.execute("SELECT name FROM star_wars.dbo.planet WHERE name='Tatooine';").fetchone()
        result = result[0]
        cursor.close()
        connection.close()

        # Assert query result
        self.assertEqual(result, 'Tatooine')

    def test_get_connection_oracle_12c(self):
        """Unit tests for method get_connection for Oracle database."""

        # Set connection parameters
        data_source_type_id = DataSourceType.ORACLE_ID
        connection_string = 'driver={Oracle 12c};server=oracle;port=1521;Database=star_wars;'
        login = 'system'
        password = 'oracle'

        # Connect to test Database
        data_source = DataSource()
        connection = data_source.get_connection(data_source_type_id, connection_string, login, password)
        cursor = connection.cursor()
        result = cursor.execute("SELECT name FROM star_wars.planet WHERE name='Tatooine';").fetchone()
        result = result[0]
        cursor.close()
        connection.close()

        # Assert query result
        self.assertEqual(result, 'Tatooine')

    def test_get_connection_postgresql(self):
        """Unit tests for method get_connection for PostgreSQL database."""

        # Set connection parameters
        data_source_type_id = DataSourceType.POSTGRESQL_ID
        connection_string = 'driver={PostgreSQL Unicode};server=db-postgresql;port=5432;Database=star_wars;'
        login = 'postgres'
        password = '1234'

        # Connect to test Database
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
        """Unit tests for method get_connection for SQLite database."""

        # Set connection parameters
        data_source_type_id = DataSourceType.SQLITE_ID
        connection_string = './star_wars.db'

        # Connect to test Database
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
        """Unit tests for method get_connection for Teradata database."""
        pass


if __name__ == '__main__':
    unittest.main()
