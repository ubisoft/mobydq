#!/usr/bin/env python
"""Setup data quality framework instance."""
from ast import literal_eval
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
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
    # Create configuration file
    file_name = 'data_quality.cfg'  # Default configuration file name
    log.info('Create configuration file {}'.format(file_name))
    configuration = configparser.ConfigParser()

    # Api default configuration
    configuration['api'] = {}
    configuration['api']['host'] = socket.gethostname()
    configuration['api']['port'] = '5000'  # Default port used by flask for the api

    # Web app default configuration
    configuration['app'] = {}
    configuration['app']['host'] = socket.gethostname()
    configuration['app']['port'] = '5001'  # Port must be different from the api

    # Database default configuration
    configuration['database'] = {}
    configuration['database']['secret_key'] = Fernet.generate_key().decode('utf-8')

    # Mail configuration
    configuration['mail'] = {}
    configuration['mail']['host'] = 'change_me'
    configuration['mail']['port'] = 'change_me'
    configuration['mail']['sender'] = 'change_me'

    # Write configuration in flat file
    with open(file_name, 'w') as config_file:
        configuration.write(config_file)

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
                    Operation(object['class']).create(**record)
