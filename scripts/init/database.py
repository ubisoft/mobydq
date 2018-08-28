import logging
import pyodbc
import sqlite3

# Load logging configuration
log = logging.getLogger(__name__)


class Database:
    """Database class."""

    def __init__(self):
        pass

    @staticmethod
    def get_connection(data_source_type_id, connection_string, login=None, password=None):
        """Connect to a data source. Return a connection object."""
        # Add login to connection string if it is not empty
        if login:
            connection_string = connection_string + 'uid={login};'.format(login=login)

        # Add password to connection string if it is not empty
        if password:
            connection_string = connection_string + 'pwd={password};'.format(password=password)

        # Hive
        if data_source_type_id == 1:
            connection = pyodbc.connect(connection_string)
            connection.setencoding(encoding='utf-8')

        # Impala
        elif data_source_type_id == 2:
            connection = pyodbc.connect(connection_string)
            connection.setencoding(encoding='utf-8')

        # MariaDB
        elif data_source_type_id == 3:
            connection = pyodbc.connect(connection_string)

        # Microsoft SQL Server
        elif data_source_type_id == 4:
            connection = pyodbc.connect(connection_string)

        # MySQL
        elif data_source_type_id == 5:
            connection = pyodbc.connect(connection_string)

        # Oracle
        elif data_source_type_id == 6:
            connection = pyodbc.connect(connection_string)

        # PostgreSQL
        elif data_source_type_id == 7:
            connection = pyodbc.connect(connection_string)
            connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            connection.setencoding(encoding='utf-8')

        # SQLite
        elif data_source_type_id == 8:
            connection = sqlite3.connect(connection_string)

        # Teradata
        elif data_source_type_id == 9:
            connection = pyodbc.connect(connection_string)
            connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            connection.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
            connection.setencoding(encoding='utf-8')

        return connection
