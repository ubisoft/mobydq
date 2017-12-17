#!/usr/bin/env python
"""Functions to perform database operations."""
from contextlib import contextmanager
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import logging
import os
import sys

# Import database classes
from .base import Base
from .batch import BatchOwner, Batch
from .data_source import DataSourceType, DataSource
from .event import EventType, Event
from .session import Session
from .status import Status
from .indicator import IndicatorType, Indicator, IndicatorParameter, IndicatorResult


# Load logging configuration
log = logging.getLogger(__name__)


class Operation:
    """Set of functions used to perform create, read, update or delete operations in the database."""

    def __init__(self, object):
        """Initialize class."""
        db_path = os.path.join(os.path.dirname(__file__), 'data_quality.db')
        db_uri = 'sqlite:///{}'.format(db_path)
        engine = create_engine(db_uri)

        # Bind engine to metadata of the base class
        Base.metadata.bind = engine

        # Create database session object
        self.dbSession = sessionmaker(bind=engine, expire_on_commit=False)

        # Get class of the object on which to perform operations
        self.object = getattr(sys.modules[__name__], object)

    @contextmanager
    def open_session(self):
        """Open database session."""
        session = self.dbSession()
        yield session
        session.close()

    @staticmethod
    def get_parameter(section, parameter_name=None):
        configuration = configparser.ConfigParser()
        path = os.path.dirname(__file__)
        configuration.read(path + '/database.cfg')
        if parameter_name:
            parameters = configuration[section][parameter_name]
        else:
            parameters = {}
            for key in configuration[section]:
                parameters[key] = configuration[section][key]
        return parameters

    @staticmethod
    def encryption(action, value):
        secret_key = Operation.get_parameter('database', 'secret_key')
        cipher = Fernet(secret_key.encode('utf-8'))
        if action == 'encrypt':
            value = cipher.encrypt(value.encode('utf-8'))
        elif action == 'decrypt':
            value = cipher.decrypt(value.encode('utf-8'))
        value = value.decode('utf-8')
        return value

    def create(self, **kwargs):
        """Create record. Return list of objects."""
        with self.open_session() as session:
            # Apply encryption on password fields
            for key in kwargs:
                if key == 'password' and kwargs[key] != '':
                    kwargs[key] = Operation.encryption('encrypt', kwargs[key])

            instance = self.object(**kwargs)
            session.add(instance)
            session.commit()
            log.debug('{} created with values: {}'.format(self.object.__name__, kwargs))

            # Return object
            instance = session.query(self.object).filter_by(id=instance.id).first()
        return instance

    def read(self, **kwargs):
        """Get record or list of records. Return list of objects."""
        with self.open_session() as session:
            instance = session.query(self.object).filter_by(**kwargs).all()
            log.debug('Select {} returned {} records'.format(self.object.__name__, len(instance)))

        # Return list of objects
        return instance

    def update(self, **kwargs):
        """Update record. Return list of objects."""
        with self.open_session() as session:
            # Verify record exists
            instance = session.query(self.object).filter_by(id=kwargs['id']).first()
            if not instance:
                log.error('No {} found with Id: {}'.format(self.object.__name__, kwargs['id']))
            else:
                # Apply encryption on password fields
                for key in kwargs:
                    if key == 'password' and kwargs[key] != '':
                        kwargs[key] = Operation.encryption('encrypt', kwargs[key])

                    # if password is emmpty, do not overwrite existing value
                    elif key == 'password' and kwargs[key] != '':
                        del kwargs[key]

                instance = session.query(self.object).filter_by(id=kwargs['id']).update(kwargs)
                session.commit()
                log.debug('{} with Id {} updated'.format(self.object.__name__, kwargs['id']))

            # Return object
            instance = session.query(self.object).filter_by(id=kwargs['id']).first()
        return instance

    def delete(self, **kwargs):
        """Delete record. Return empty list of objects."""
        with self.open_session() as session:
            # Verify record exists
            instance = session.query(self.object).filter_by(**kwargs).first()
            if not instance:
                log.error('No {} found with values: {}'.format(self.object.__name__, kwargs))
            else:
                instance = session.query(self.object).filter_by(**kwargs).delete()
                session.commit()
                log.debug('{} with values {} deleted'.format(self.object.__name__, kwargs))

        # Return empty object
        return instance
