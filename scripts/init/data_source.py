import logging
import pyodbc
import sqlite3
import traceback
import utils
from constants import Database

# Load logging configuration
log = logging.getLogger(__name__)


class DataSource:
    """Data source class."""

    def get_connection(self, data_source_type_id: int, connection_string: str, login: str = None, password: str = None):
        """Connect to a data source. Return a connection object."""
        # Add login to connection string if it is not empty
        if login:
            connection_string = connection_string + \
                'uid={login};'.format(login=login)

        # Add password to connection string if it is not empty
        if password:
            connection_string = connection_string + \
                'pwd={password};'.format(password=password)

        # Hive
        if data_source_type_id == Database.HIVE_ID:
            connection = pyodbc.connect(connection_string)
            connection.setencoding(encoding='utf-8')

        # Impala
        elif data_source_type_id == Database.IMPALA_ID:
            connection = pyodbc.connect(connection_string)
            connection.setencoding(encoding='utf-8')

        # MariaDB
        elif data_source_type_id == Database.MARIADB_ID:
            connection = pyodbc.connect(connection_string)

        # Microsoft SQL Server
        elif data_source_type_id == Database.MSSQL_ID:
            connection = pyodbc.connect(connection_string)

        # MySQL
        elif data_source_type_id == Database.MYSQL_ID:
            connection = pyodbc.connect(connection_string)

        # Oracle
        elif data_source_type_id == Database.ORACLE_ID:
            connection = pyodbc.connect(connection_string)

        # PostgreSQL
        elif data_source_type_id == Database.POSTGRESQL_ID:
            connection = pyodbc.connect(connection_string)
            connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            connection.setencoding(encoding='utf-8')

        # SQLite
        elif data_source_type_id == Database.SQLITE_ID:
            connection = sqlite3.connect(connection_string)

        # Teradata
        elif data_source_type_id == Database.TERADATA_ID:
            connection = pyodbc.connect(connection_string)
            connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            connection.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
            connection.setencoding(encoding='utf-8')

        else:
            message = f'Invalid data source type with id {data_source_type_id}'
            log.error(message)
            raise ValueError(message)

        return connection

    def test(self, data_source_id: int):
        log.info('Test connectivity to data source Id {data_source_id}.'.format(
            data_source_id=data_source_id))

        # Get data source
        log.debug('Get data source.')
        query = '''query{dataSourceById(id:data_source_id){dataSourceTypeId,connectionString,login,password}}'''
        query = query.replace('data_source_id', str(
            data_source_id))  # Use replace() instead of format() because of curly braces
        response = utils.execute_graphql_request(query)

        if response['data']['dataSourceById']:
            data_source = response['data']['dataSourceById']
            data_source_type_id = data_source['dataSourceTypeId']
            connection_string = data_source['connectionString']
            login = data_source['login']
            password = data_source['password']

            # Test connectivity
            try:
                log.debug('Connect to data source.')
                self.get_connection(data_source_type_id,
                                    connection_string, login, password)

                log.info('Connection to data source succeeded.')
                mutation = '''mutation{updateDataSourceById(input:{id:data_source_id,dataSourcePatch:{connectivityStatus:"Success"}}){dataSource{connectivityStatus}}}'''
                mutation = mutation.replace('data_source_id', str(
                    data_source_id))  # Use replace() instead of format() because of curly braces
                utils.execute_graphql_request(mutation)

            except Exception:
                log.error('Connection to data source failed.')
                error_message = traceback.format_exc()
                log.error(error_message)

                # Update connectivity status
                mutation = '''mutation{updateDataSourceById(input:{id:data_source_id,dataSourcePatch:{connectivityStatus:"Failed"}}){dataSource{connectivityStatus}}}'''
                mutation = mutation.replace('data_source_id', str(
                    data_source_id))  # Use replace() instead of format() because of curly braces
                utils.execute_graphql_request(mutation)

        else:
            error_message = 'Data source Id {data_source_id} does not exist.'.format(
                data_source_id=data_source_id)
            log.error(error_message)
            raise Exception(error_message)
