#!/usr/bin/env python
"""Setup data quality framework instance."""
import argparse
from ast import literal_eval
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, exc
import configparser
from datetime import datetime
import logging
import os
import socket
import sys

# Import database classes
from api.database.base import Base
from api.database.operation import Operation

# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    # filename='data_quality.log',
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


parser = argparse.ArgumentParser(description='Show transversal xml properties.')
parser.add_argument('--force', '-f', dest='force',
                    action='store_true',
                    help='Force database reset if it already exists.')


def gen_db_config_file(db_config_file):
    # Generate database default configuration
    configuration = configparser.ConfigParser()
    configuration['database'] = {}
    configuration['database']['secret_key'] = Fernet.generate_key().decode('utf-8')

    # Write configuration in flat file
    log.info('Create configuration file: {}'.format(db_config_file))
    with open(db_config_file, 'w+') as config_file:
        configuration.write(config_file)


def gen_api_config_file(api_config_file):
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


def gen_app_config_file(app_config_file):
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


def create_db(db_name):
    db_path = os.path.join(os.path.dirname(__file__), db_name)
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


if __name__ == '__main__':
    args = parser.parse_args()
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    # Test if configuration file for the database exists
    db_config_file = 'api/database/database.cfg'
    if os.path.isfile(db_config_file):
        log.info('Database configuration file already exist: {}'.format(db_config_file))
        if args.force:
            log.info('Backuping and replacing database config')
            svg_path = 'api/database/database_%s.cfg' % ts
            os.rename(db_config_file, svg_path)
            gen_db_config_file(db_config_file)
        else:
            sys.exit(0)
    else:
        gen_db_config_file(db_config_file)

    # Test if configuration file for the api exists
    api_config_file = 'api/api.cfg'
    if os.path.isfile(api_config_file):
        log.info('API configuration file already exist: {}'.format(api_config_file))
        if args.force:
            log.info('Backuping and replacing api config')
            svg_path = 'api/api_%s.cfg' % ts
            os.rename(api_config_file, svg_path)
            gen_api_config_file(api_config_file)
        else:
            sys.exit(0)
    else:
        gen_api_config_file(api_config_file)

    # Test if configuration file for the web app exists
    app_config_file = 'app/app.cfg'
    if os.path.isfile(app_config_file):
        log.info('App configuration file already exist: {}'.format(app_config_file))
        if args.force:
            log.info('Backuping and replacing app config')
            svg_path = 'app/app_%s.cfg' % ts
            os.rename(app_config_file, svg_path)
            gen_app_config_file(app_config_file)
        else:
            sys.exit(0)
    else:
        gen_app_config_file(app_config_file)

    # Create database
    db_name = 'api/database/data_quality.db'  # Default database name
    if os.path.isfile(db_name):
        log.info('Database already exist: {}'.format(db_name))
        if args.force:
            log.info('Backuping and replacing current database')
            svg_path = 'api/database/data_quality_%s.db' % ts
            os.rename(db_name, svg_path)
            create_db(db_name)
        else:
            sys.exit(0)
    else:
        create_db(db_name)
