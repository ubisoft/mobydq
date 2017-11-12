from ast import literal_eval
from cryptography.fernet import Fernet
import configparser
import database
import logging
import os
import utils

# Load logger
utils.config_logger()
log = logging.getLogger(__name__)


if __name__ == '__main__':
    # Create local configuration file
    log.info('Create configuration file data_quality.cfg')
    configuration = configparser.ConfigParser()
    configuration['data_quality'] = {}
    configuration['data_quality']['secret_key'] = Fernet.generate_key().decode('utf-8')
    with open('data_quality.cfg', 'w') as config_file:
        configuration.write(config_file)

    # Create database
    db_path = os.path.join(os.path.dirname(__file__), 'data_quality.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    engine = database.create_engine(db_uri)

    # Create tables
    log.info('Create database data_quality.db')
    database.Base.metadata.create_all(engine)

    # Insert default list of values
    with open('data_quality.json', 'r') as data_file:
        data_dictionary = literal_eval(data_file.read())
        for object in data_dictionary['list_of_values']:
                log.info('Insert default list of values for: {}'.format(object['class']))
                for record in object['records']:
                    database.DbOperation(object['class']).create(**record)
