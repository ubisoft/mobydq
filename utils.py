"""Utility functions used by the data quality framework."""
import inspect
import logging
import pyodbc
import re
import sys
import ntpath


def config_logger():
    """Load logging configuration."""
    logging.basicConfig(
        # filename='data_quality.log',
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_file_name(path):
    """Extract file name from absolute path."""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_object_attributes(object):
    """Get attributes and their values from the instance of a class and returns them as a dictionary."""
    attributes = inspect.getmembers(object, lambda a: not(inspect.isroutine(a)))
    dictionary = {}
    for attribute in attributes:
        # Exclude object attributes belonging to sqlachemy and database classes
        if not attribute[0].startswith('_') and not re.search("<class 'sqlalchemy*|<class 'database*", str(type(attribute[1]))):
                dictionary[attribute[0]] = str(attribute[1])
    return dictionary


def get_odbc_connection(data_source):
    """Get connection string and credentials for the corresponding data source, connects to it using an ODBC connection and return a connection object."""
    connection_string = data_source.connectionString
    connection_string = connection_string + 'uid=' + data_source.login
    connection_string = connection_string + ';pwd=' + data_source.password + ';'
    connection = pyodbc.connect(connection_string)

    # Teradata
    if data_source.dataSourceTypeId == 1:
        connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
        connection.setencoding(encoding='utf-8')
    return connection
