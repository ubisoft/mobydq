#!/usr/bin/env python
"""Setup data quality framework instance."""
from ast import literal_eval
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
import configparser
import logging
import os
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
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    # Create local configuration file
    log.info('Create configuration file data_quality.cfg')
    configuration = configparser.ConfigParser()
    configuration['data_quality'] = {}
    configuration['data_quality']['secret_key'] = Fernet.generate_key().decode('utf-8')
    with open('api/database/data_quality.cfg', 'w') as config_file:
        configuration.write(config_file)

    # Create database
    db_path = os.path.join(os.path.dirname(__file__), 'api/database/data_quality.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    engine = create_engine(db_uri)

    # Create tables
    log.info('Create database data_quality.db')
    Base.metadata.create_all(engine)

    # Insert default list of values
    with open('api/database/data.json', 'r') as data_file:
        data_dictionary = literal_eval(data_file.read())
        for object in data_dictionary['list_of_values']:
                log.info('Insert default list of values for: {}'.format(object['class']))
                for record in object['records']:
                    Operation(object['class']).create(**record)
