#!/usr/bin/env python
"""Setup data quality framework database and perform CRUD operations."""
from ast import literal_eval
from sqlalchemy import create_engine
import logging
import os
import sys

from database.base import Base
from database.operation import Operation as DbOperation

log = logging.getLogger(__name__)


logging.basicConfig(
    # filename='data_quality.log',
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    db_path = os.path.join(os.path.dirname(__file__), 'data_quality.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    engine = create_engine(db_uri)

    # Create all tables in the engine
    log.info('Create database and tables')
    Base.metadata.create_all(engine)

    # Insert default list of values
    with open('data_quality.json', 'r') as data_file:
        data_dictionary = literal_eval(data_file.read())
        for object in data_dictionary['list_of_values']:
                log.info('Insert default list of values for: {}'.format(object['class']))
                for record in object['records']:
                    DbOperation(object['class']).create(**record)
