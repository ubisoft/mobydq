#!/usr/bin/env python
"""Functions related to data source objects."""
from .database.operation import Operation
import logging
import pandas
import pyodbc
import sqlite3

# Load logging configuration
log = logging.getLogger(__name__)


class DataSourceMethod:
    def __init__(self, data_source_name):
        """Initialize class."""
        # Initialize dictionary for error message
        self.error_message = {}

        # Verify data source exists
        data_source_list = Operation('DataSource').read(name=data_source_name)

        if data_source_list:
            self.data_source = data_source_list[0]
        else:
            self.error_message['message'] = 'No {} found with values: {}'.format('DataSource', {'name': data_source_name})
            log.error(self.error_message['message'])
            return self.error_message

    def get_database_connection(self):
        """Connect to a data source of type database using an ODBC connection. Return a connection object."""
        connection_string = self.data_source.connectionString

        # Add login to connection string if it is not empty
        if self.data_source.login:
            connection_string = connection_string + 'uid={};'.format(self.data_source.login)

        # Add password to connection string if it is not empty
        if self.data_source.password:
            connection_string = connection_string + 'pwd={};'.format(self.data_source.password)

        # Hive
        if self.data_source.dataSourceTypeId == 1:
            connection = pyodbc.connect(connection_string)
            connection.setencoding(encoding='utf-8')

        # Impala
        if self.data_source.dataSourceTypeId == 2:
            connection = pyodbc.connect(connection_string)
            connection.setencoding(encoding='utf-8')

        # Microsoft SQL Server
        if self.data_source.dataSourceTypeId == 3:
            connection = pyodbc.connect(connection_string)
            pass

        # MySQL
        if self.data_source.dataSourceTypeId == 4:
            connection = pyodbc.connect(connection_string)
            pass

        # PostgreSQL
        if self.data_source.dataSourceTypeId == 5:
            connection = pyodbc.connect(connection_string)
            pass

        # SQLite
        if self.data_source.dataSourceTypeId == 6:
            connection = sqlite3.connect(connection_string)

        # Teradata
        if self.data_source.dataSourceTypeId == 7:
            connection = pyodbc.connect(connection_string)
            connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            connection.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
            connection.setencoding(encoding='utf-8')
        return connection

    def get_data_frame(self, request):
        """Connect to a data source, execute request and return the corresponding results as a pandas data frame."""

        # Identify the type of data source
        data_source_type_list = Operation('DataSourceType').read(id=self.data_source.dataSourceTypeId)

        if data_source_type_list:
            data_source_type = data_source_type_list[0]
        else:
            self.error_message['message'] = 'No {} found with values: {}'.format('DataSourceType', {'id': self.data_source.dataSourceTypeId})
            log.error(self.error_message['message'])
            return self.error_message

        # Database
        if data_source_type.type == 'Database':
            connection = self.get_database_connection()
            data_frame = pandas.read_sql(request, connection)

        # File
        elif data_source_type.type == 'File':
            # Not implemented yet
            pass

        # API
        elif data_source_type.type == 'API':
            # Not implemented yet
            pass

        else:
            self.error_message['message'] = 'Unknown data source type: {}'.format(data_source_type.type)
            log.error(self.error_message['message'])
            return self.error_message

        return data_frame
