"""Utility functions used by the data quality framework."""
from cryptography.fernet import Fernet
import configparser
import inspect
import logging
import os
import pyodbc
import re
import sqlite3
import sys


def config_logger():
    """Load logging configuration."""
    logging.basicConfig(
        # filename='data_quality.log',
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_parameter(section, parameter_name=None):
    configuration = configparser.ConfigParser()
    configuration.read(os.path.dirname(__file__) + '/data_quality.cfg')
    if parameter_name:
        parameters = configuration[section][parameter_name]
    else:
        parameters = {}
        for key in configuration[section]:
            parameters[key] = configuration[section][key]
    return parameters


def get_object_attributes(object):
    """Get attributes and their values from the instance of a class and returns them as a dictionary."""
    attributes = inspect.getmembers(object, lambda a: not(inspect.isroutine(a)))
    dictionary = {}
    for attribute in attributes:
        # Exclude object attributes belonging to sqlachemy and database classes
        if not attribute[0].startswith('_') and not re.search("<class 'sqlalchemy*|<class 'database*", str(type(attribute[1]))):
                dictionary[attribute[0]] = str(attribute[1])
    return dictionary


def encryption(action, value):
    secret_key = get_parameter('data_quality', 'secret_key')
    cipher = Fernet(secret_key.encode('utf-8'))
    if action == 'encrypt':
        value = cipher.encrypt(value.encode('utf-8'))
    elif action == 'decrypt':
        value = cipher.decrypt(value.encode('utf-8'))
    value = value.decode('utf-8')
    return value


def get_database_connection(data_source):
    """
    Get connection string and credentials for the corresponding data source,
    connects to it using an ODBC connection and return a connection object.
    """
    connection_string = data_source.connectionString

    # Add login to connection string if it is not empty
    if data_source.login:
        connection_string = connection_string + 'uid={};'.format(data_source.login)

    # Add password to connection string if it is not empty
    if data_source.password:
        connection_string = connection_string + 'pwd={};'.format(data_source.password)

    # Hive
    if data_source.dataSourceTypeId == 1:
        connection = pyodbc.connect(connection_string)
        connection.setencoding(encoding='utf-8')

    # Impala
    if data_source.dataSourceTypeId == 2:
        connection = pyodbc.connect(connection_string)
        connection.setencoding(encoding='utf-8')

    # Microsoft SQL Server
    if data_source.dataSourceTypeId == 3:
        connection = pyodbc.connect(connection_string)
        pass

    # MySQL
    if data_source.dataSourceTypeId == 4:
        connection = pyodbc.connect(connection_string)
        pass

    # PostgreSQL
    if data_source.dataSourceTypeId == 5:
        connection = pyodbc.connect(connection_string)
        pass

    # SQLite
    if data_source.dataSourceTypeId == 6:
        connection = sqlite3.connect(connection_string)

    # Teradata
    if data_source.dataSourceTypeId == 7:
        connection = pyodbc.connect(connection_string)
        connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
        connection.setencoding(encoding='utf-8')
    return connection
