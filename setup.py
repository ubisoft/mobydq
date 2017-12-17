#!/usr/bin/env python
"""Setup data quality framework instance."""
from ast import literal_eval
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, exc
import configparser
import logging
import os
import socket
import sys

# Import database classes
from api.database.base import Base
from api.database.data_source import DataSourceType, DataSource
from api.database.session import Session
from api.database.operation import Operation

# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    # filename='data_quality.log',
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    # Test if configuration file for the database exists
    db_config_file = 'api/database/database.cfg'
    if not os.path.isfile(db_config_file):
        # Generate database default configuration
        configuration = configparser.ConfigParser()
        configuration['database'] = {}
        configuration['database']['secret_key'] = Fernet.generate_key().decode('utf-8')

        # Write configuration in flat file
        log.info('Create configuration file: {}'.format(db_config_file))
        with open(db_config_file, 'w+') as config_file:
            configuration.write(config_file)
    else:
        log.info('Configuration file already exist: {}'.format(db_config_file))

    # Test if configuration file for the api exists
    api_config_file = 'api/api.cfg'
    if not os.path.isfile(api_config_file):
        # Generate default api configuration
        configuration = configparser.ConfigParser()
        configuration['api'] = {}
        configuration['api']['host'] = socket.gethostname()
        configuration['api']['port'] = '5000'  # Default port used by flask for the api
        configuration['mail'] = {}
        configuration['mail']['host'] = 'change_me'
        configuration['mail']['port'] = 'change_me'
        configuration['mail']['sender'] = 'change_me'

        # Write configuration in flat file
        log.info('Create configuration file: {}'.format(api_config_file))
        with open(api_config_file, 'w+') as config_file:
            configuration.write(config_file)
    else:
        log.info('Configuration file already exist: {}'.format(api_config_file))

    # Test if configuration file for the web app exists
    app_config_file = 'app/app.cfg'
    if not os.path.isfile(app_config_file):
        # Generate default web app configuration
        configuration = configparser.ConfigParser()
        configuration['api'] = {}  # Repeat api configuration for the web app to know where to send http requests
        configuration['api']['host'] = socket.gethostname()
        configuration['api']['port'] = '5000'  # Default port used by flask for the api
        configuration['app'] = {}
        configuration['app']['host'] = socket.gethostname()
        configuration['app']['port'] = '5001'  # Port must be different from the api

        # Write configuration in flat file
        log.info('Create configuration file: {}'.format(app_config_file))
        with open(app_config_file, 'w+') as config_file:
            configuration.write(config_file)
    else:
        log.info('Configuration file already exist: {}'.format(app_config_file))

    # Create database
    db_name = 'data_quality.db'  # Default database name
    db_path = os.path.join(os.path.dirname(__file__), 'api/database/{}'.format(db_name))
    db_uri = 'sqlite:///{}'.format(db_path)
    engine = create_engine(db_uri)

    # Create tables
    log.info('Create database {}'.format(db_name))
    Base.metadata.create_all(engine)

    # Insert default list of values
    with open('api/database/data.json', 'r') as data_file:
        data_dictionary = literal_eval(data_file.read())
        for object in data_dictionary['list_of_values']:
                log.info('Insert default list of values for: {}'.format(object['class']))
                for record in object['records']:
                    try:
                        Operation(object['class']).create(**record)
                    except exc.IntegrityError:
                        log.info('Record already exist: {}'.format(record))
