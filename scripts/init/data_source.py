"""Manage class and methods for data sources."""
import logging
import sqlite3
import traceback
import pyodbc
import utils
from constants import DataSourceType

# Load logging configuration
log = logging.getLogger(__name__)


class DataSource:
    """Data source class."""

    def get_connection(self, data_source_type_id: int, connection_string: str, login: str = None, password: str = None):
        """Connect to a data source. Return a connection object."""

        # Add login to connection string if it is not empty
        if login:
            connection_string = f'{connection_string}uid={login};'

        # Add password to connection string if it is not empty
        if password:
            connection_string = connection_string = f'{connection_string}pwd={password};'

        # Create connection object for SQLite
        if data_source_type_id == DataSourceType.SQLITE_ID:
            connection = sqlite3.connect(connection_string)

        # Create connection object for all other data source types using pyodbc
        else:
            connection = pyodbc.connect(connection_string)

        # Cloudera Hive
        if data_source_type_id == DataSourceType.CLOUDERA_HIVE_ID:
            connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            connection.setencoding(encoding='utf-8')

        # Cloudera Impala
        elif data_source_type_id == DataSourceType.CLOUDERA_IMPALA_ID:
            connection.setencoding(encoding='utf-8')

        # Hortonworks Hive
        elif data_source_type_id == DataSourceType.HORTONWORKS_HIVE_ID:
            connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            connection.setencoding(encoding='utf-8')

        # MariaDB
        # elif data_source_type_id == DataSourceType.MARIADB_ID:
        #     Do nothing

        # Microsoft SQL Server
        # elif data_source_type_id == DataSourceType.MSSQL_ID:
        #     Do nothing

        # MySQL
        # elif data_source_type_id == DataSourceType.MYSQL_ID:
        #     Do nothing

        # Oracle
        # elif data_source_type_id == DataSourceType.ORACLE_ID:
        #     Do nothing

        # PostgreSQL
        elif data_source_type_id == DataSourceType.POSTGRESQL_ID:
            connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            connection.setencoding(encoding='utf-8')

        # Snowflake
        # elif data_source_type_id == DataSourceType.SNOWFLAKE_ID:
        #     Do nothing

        # SQLite
        # elif data_source_type_id == DataSourceType.SQLITE_ID:
        #     Do nothing

        # Teradata
        elif data_source_type_id == DataSourceType.TERADATA_ID:
            connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            connection.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
            connection.setencoding(encoding='utf-8')

        return connection

    def get_password(self, authorization: str, data_source_id: int):
        """Get unencrypted password of a data source. Return the password."""

        query = 'query getDataSourcePassword($id: Int){allDataSourcePasswords(condition:{id: $id}){nodes{password}}}'
        variables = {'id': data_source_id}
        payload = {'query': query, 'variables': variables}
        response = utils.execute_graphql_request(authorization, payload)

        if response['data']['allDataSourcePasswords']['nodes']:
            data_source = response['data']['allDataSourcePasswords']['nodes'][0]
            password = data_source['password']

        else:
            error_message = f'Data source {data_source_id} does not exist.'
            log.error(error_message)
            raise Exception(error_message)

        return password

    def test(self, authorization: str, data_source_id: int):
        """Test connectivity to a data source and update its connectivity status."""
        log.info('Test connectivity to data source Id %i.', data_source_id)

        # Set connectivity test to running
        query = 'mutation updateDataSourceStatus($id: Int!, $dataSourcePatch: DataSourcePatch!){updateDataSourceById(input:{id: $id, dataSourcePatch: $dataSourcePatch}){dataSource{connectivityStatus}}}'
        variables = {'id': data_source_id, 'dataSourcePatch': {'connectivityStatus': 'Running'}}
        payload = {'query': query, 'variables': variables}
        utils.execute_graphql_request(authorization, payload)

        # Get data source
        log.debug('Get data source.')
        query = 'query getDataSource($id: Int!){dataSourceById(id: $id){dataSourceTypeId, connectionString, login}}'
        variables = {'id': data_source_id}
        payload = {'query': query, 'variables': variables}
        response = utils.execute_graphql_request(authorization, payload)

        if response['data']['dataSourceById']:
            data_source = response['data']['dataSourceById']
            data_source_type_id = data_source['dataSourceTypeId']
            connection_string = data_source['connectionString']
            login = data_source['login']

        # Get data source password
        password = self.get_password(authorization, data_source_id)

        # Test connectivity
        try:
            log.debug('Connect to data source.')
            self.get_connection(data_source_type_id, connection_string, login, password)

            log.info('Connection to data source succeeded.')
            query = 'mutation updateDataSourceStatus($id: Int!, $dataSourcePatch: DataSourcePatch!){updateDataSourceById(input:{id: $id, dataSourcePatch: $dataSourcePatch}){dataSource{connectivityStatus}}}'
            variables = {'id': data_source_id, 'dataSourcePatch': {'connectivityStatus': 'Success'}}
            payload = {'query': query, 'variables': variables}
            utils.execute_graphql_request(authorization, payload)

        except Exception:  # Pylint: disable=broad-except
            log.error('Connection to data source failed.')
            error_message = traceback.format_exc()
            log.error(error_message)

            # Update connectivity status
            query = 'mutation updateDataSourceStatus($id: Int!, $dataSourcePatch: DataSourcePatch!){updateDataSourceById(input:{id: $id, dataSourcePatch: $dataSourcePatch}){dataSource{connectivityStatus}}}'
            variables = {'id': data_source_id, 'dataSourcePatch': {'connectivityStatus': 'Failed'}}
            payload = {'query': query, 'variables': variables}
            utils.execute_graphql_request(authorization, payload)
