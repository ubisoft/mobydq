"""Unit tests for module /scripts/init/data_source.py."""
import unittest
from shared.utils import get_authorization
from scripts.data_source import DataSource
from scripts.constants import DataSourceType


class TestDataSource(unittest.TestCase):
    """Unit tests for class DataSource."""

    def test_get_password(self):
        """Unit tests for method get_password."""

        # Authenticate user
        authorization = get_authorization()

        # Get password for Cloudera Hive data source
        data_source = DataSource()
        password = data_source.get_password(authorization, 1)

        # Assert query result
        self.assertEqual(password, 'cloudera')

    def test_get_connection_cloudera_hive(self):
        """Unit tests for method get_connection for Cloudera Hive database."""

        # Set connection parameters
        data_source_type_id = DataSourceType.CLOUDERA_HIVE_ID
        connection_string = 'driver={Cloudera Hive};Host=db-cloudera;Port=10000;'
        login = 'cloudera'
        password = 'cloudera'

        # Connect to test Database
        data_source = DataSource()
        connection = data_source.get_connection(data_source_type_id, connection_string, login, password)
        cursor = connection.cursor()
        result = cursor.execute("SELECT name FROM star_wars.planet WHERE name='Tatooine'").fetchone()
        result = result[0]
        cursor.close()
        connection.close()

        # Assert query result
        self.assertEqual(result, 'Tatooine')

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

    def test_get_connection_mysql(self):
        """Unit tests for method get_connection for MySQL database."""

        # Set connection parameters
        data_source_type_id = DataSourceType.MYSQL_ID
        connection_string = 'driver={MySQL Unicode};server=db-mysql;port=3306;Database=star_wars;'
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

    # def test_get_connection_oracle(self):
        # """Unit tests for method get_connection for Teradata database."""
        # TODO: Not implemented because Oracle Docker container is too heavy
        # pass

    # def test_get_connection_teradata(self):
        # """Unit tests for method get_connection for Teradata database."""
        # TODO: Not implemented because there is no Teradata Docker image
        # pass
    
     # def test_get_connection_snowflake(self):
        # """Unit tests for method get_connection for Snowflake database."""
        # TODO: Not implemented because there is no Snowflake Docker image
        # pass
    
    # def test_get_connection_hortonworks_hive(self):
        # """Unit tests for method get_connection for Hortonworks Hive database."""
        # TODO: To be implemented
        # pass


if __name__ == '__main__':
    unittest.main()
