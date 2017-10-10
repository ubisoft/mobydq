"""Setup data quality framework database and perform CRUD operations."""
from ast import literal_eval
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, TypeDecorator
from sqlalchemy import create_engine
from sqlalchemy.ext import mutable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
import argparse
import json
import logging
import sys
import utils

# Load logger
utils.configlogger()
log = logging.getLogger(__name__)


class JsonEncodedDict(TypeDecorator):
    """Create custom data type to enable json storage in event table."""

    impl = String

    def process_bind_param(self, value, dialect):
        """Dump."""
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        """Load."""
        return json.loads(value)

mutable.MutableDict.associate_with(JsonEncodedDict)

# Declarative base model to create database tables and classes
Base = declarative_base()


class Status(Base):
    """Status for batches and sessions."""

    __tablename__ = 'status'

    id = Column('status_id', Integer, primary_key=True)
    name = Column('status', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    batch = relationship('Batch', backref='Status')
    session = relationship('Session', backref='Status')


class DataSourceType(Base):
    """Types of data sources."""

    __tablename__ = 'data_source_type'

    id = Column('data_source_type_id', Integer, primary_key=True)
    name = Column('data_source_type', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    dataSource = relationship('DataSource', backref='DataSourceType')


class DataSource(Base):
    """Data sources."""

    __tablename__ = 'data_source'

    id = Column('data_source_id', Integer, primary_key=True)
    name = Column('data_source', String, nullable=False, unique=True)
    dataSourceTypeId = Column('data_source_type_id', Integer, ForeignKey('data_source_type.data_source_type_id'), nullable=False)
    connectionString = Column('connection_string', String)
    login = Column('login', String)
    password = Column('password', String)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())


class BatchOwner(Base):
    """Batch owners."""

    __tablename__ = 'batch_owner'

    id = Column('batch_owner_id', Integer, primary_key=True)
    name = Column('batch_owner', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    batch = relationship('Batch', backref='BatchOwner', passive_deletes=True)
    indicator = relationship('Indicator', backref='BatchOwner')


class Batch(Base):
    """Batches."""

    __tablename__ = 'batch'

    id = Column('batch_id', Integer, primary_key=True)
    batchOwnerId = Column('batch_owner_id', Integer, ForeignKey('batch_owner.batch_owner_id', ondelete='CASCADE'), nullable=False)
    statusId = Column('status_id', Integer, ForeignKey('status.status_id'), nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    session = relationship('Session', backref='Batch', passive_deletes=True)


class IndicatorType(Base):
    """Types of indicators."""

    __tablename__ = 'indicator_type'

    id = Column('indicator_type_id', Integer, primary_key=True)
    name = Column('indicator_type', String, nullable=False, unique=True)
    module = Column('module', String, nullable=False)
    function = Column('function', String, nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    indicator = relationship('Indicator', backref='IndicatorType')


class Indicator(Base):
    """Data quality indicators."""

    __tablename__ = 'indicator'

    id = Column('indicator_id', Integer, primary_key=True)
    name = Column('indicator', String, nullable=False, unique=True)
    description = Column('indicator_description', String, nullable=False)
    indicatorTypeId = Column('indicator_type_id', Integer, ForeignKey('indicator_type.indicator_type_id'), nullable=False)
    batchOwnerId = Column('batch_owner_id', Integer, ForeignKey('batch_owner.batch_owner_id'), nullable=False)
    executionOrder = Column('execution_order', Integer, nullable=False, default=0)
    alertOperator = Column('alert_operator', String, nullable=False)
    alertThreshold = Column('alert_threshold', Float, nullable=False)
    distributionList = Column('distribution_list', String, nullable=False)
    active = Column('flag_active', Boolean, nullable=False, default=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    indicatorParameter = relationship('IndicatorParameter', backref='Indicator', passive_deletes=True)
    indicatorResult = relationship('IndicatorResult', backref='Indicator', passive_deletes=True)
    session = relationship('Session', backref='Indicator', passive_deletes=True)


class IndicatorParameter(Base):
    """Indicator parameters."""

    __tablename__ = 'indicator_parameter'

    id = Column('indicator_parameter_id', Integer, primary_key=True)
    name = Column('indicator_parameter', String, nullable=False)
    value = Column('indicator_parameter_value', String, nullable=False)
    indicatorId = Column('indicator_id', Integer, ForeignKey('indicator.indicator_id', ondelete='CASCADE'), nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())


class Session(Base):
    """Sessions."""

    __tablename__ = 'session'

    id = Column('session_id', Integer, primary_key=True)
    statusId = Column('status_id', Integer, ForeignKey('status.status_id'), nullable=False)
    indicatorId = Column('indicator_id', Integer, ForeignKey('indicator.indicator_id', ondelete='CASCADE'), nullable=False)
    batchId = Column('batch_id', Integer, ForeignKey('batch.batch_id', ondelete='CASCADE'), nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    event = relationship('Event', backref='Session', passive_deletes=True)
    indicatorResult = relationship('IndicatorResult', backref='Session', passive_deletes=True)


class EventType(Base):
    """Types of events."""

    __tablename__ = 'event_type'

    id = Column('event_type_id', Integer, primary_key=True)
    name = Column('event_type', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    event = relationship('Event', backref='EventType')


class Event(Base):
    """Events."""

    __tablename__ = 'event'

    id = Column('event_id', Integer, primary_key=True)
    eventTypeId = Column('event_type_id', Integer, ForeignKey('event_type.event_type_id'), nullable=False)
    sessionId = Column('session_id', Integer, ForeignKey('session.session_id', ondelete='CASCADE'), nullable=False)
    content = Column('content', JsonEncodedDict)
    createdDate = Column('created_date', DateTime, server_default=func.now())


class IndicatorResult(Base):
    """Indicator results."""

    __tablename__ = 'indicator_result'

    id = Column('indicator_result_id', Integer, primary_key=True)
    indicatorId = Column('indicator_id', Integer, ForeignKey('indicator.indicator_id', ondelete='CASCADE'), nullable=False)
    sessionId = Column('session_id', Integer, ForeignKey('session.session_id', ondelete='CASCADE'), nullable=False)
    alertOperator = Column('alert_operator', String, nullable=False)
    alertThreshold = Column('alert_threshold', Float, nullable=False)
    nbRecords = Column('nb_records', Integer, nullable=False)
    nbRecordsAlert = Column('nb_records_alert', Integer, nullable=False)
    nbRecordsNoAlert = Column('nb_records_no_alert', Integer, nullable=False)
    avgResult = Column('avg_result', Float, nullable=False)
    avgResultAlert = Column('avg_result_alert', Float, nullable=False)
    avgResultNoAlert = Column('avg_result_no_alert', Float, nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())


class Function:
    """Set of functions used to perform create, read, update or delete operations in the database."""

    def __init__(self, object):
        """Initialize class."""
        engine = create_engine('sqlite:///data_quality.db')

        # Bind engine to metadata of the base class
        Base.metadata.bind = engine

        # Create database session object
        self.dbsession = sessionmaker(bind=engine, expire_on_commit=False)

        # Get class of the object on which to perform operations
        self.object = getattr(sys.modules[__name__], object)

    def __enter__(self):
        """Open database session."""
        self.session = self.dbsession()
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        """Close database session."""
        self.session.close()

    def create(self, **kwargs):
        """Create record. Return list of objects."""
        if not kwargs:
            print('Enter attributes of the {} to be created in JSON format.'.format(self.object.__name__))
            print('Example {"attribute1": "Value 1", "attribute2": "Value 2"}:')
            kwargs = literal_eval(input())

        # Verify record does not exist
        instance = self.session.query(self.object).filter_by(**kwargs).first()
        if instance:
            log.error('{} already exists with values: {}'.format(self.object.__name__, kwargs))
        else:
            instance = self.object(**kwargs)
            self.session.add(instance)
            self.session.commit()
            log.info('{} created with values: {}'.format(self.object.__name__, kwargs))

        # Return list of objects
        instance = self.session.query(self.object).filter_by(**kwargs).all()
        return instance

    def read(self, **kwargs):
        """Get record or list of records. Return list of objects."""
        if not kwargs:
            print('Enter attributes of the {} to be selected in JSON format.'.format(self.object.__name__))
            print('Example {"attribute1": "Value 1", "attribute2": "Value 2"}:')
            kwargs = literal_eval(input())

        instance = self.session.query(self.object).filter_by(**kwargs).all()
        log.info('Select {} returned {} records'.format(self.object.__name__, len(instance)))

        # Return list of objects
        return instance

    def update(self, **kwargs):
        """Update record. Return list of objects."""
        if not kwargs:
            print('Enter attributes of the {} to be updated in JSON format.'.format(self.object.__name__))
            print('JSON must contain the Id of the record to be updated.')
            print('Example {"id": "1", "attribute1": "Value 1", "attribute2": "Value 2"}:')
            kwargs = literal_eval(input())

        # Verify record exists
        instance = self.session.query(self.object).filter_by(id=kwargs['id']).first()
        if not instance:
            log.error('No {} found with Id: {}'.format(self.object.__name__, kwargs['id']))
        else:
            instance = self.session.query(self.object).filter_by(id=kwargs['id']).update(kwargs)
            self.session.commit()
            log.info('{} with Id {} updated'.format(self.object.__name__, kwargs['id']))

        # Return list of objects
        instance = self.session.query(self.object).filter_by(**kwargs).all()
        return instance

    def delete(self, **kwargs):
        """Delete record. Return empty list of objects."""
        if not kwargs:
            print('Enter attributes of the {} to be deleted in JSON format.'.format(self.object.__name__))
            print('Example {"attribute1": "Value 1", "attribute2": "Value 2"}:')
            kwargs = literal_eval(input())

        # Verify record exists
        instance = self.session.query(self.object).filter_by(**kwargs).first()
        if not instance:
            log.error('No {} found with values: {}'.format(self.object.__name__, kwargs))
        else:
            instance = self.session.query(self.object).filter_by(**kwargs).delete()
            self.session.commit()
            log.info('{} with values {} deleted'.format(self.object.__name__, kwargs))

        # Return empty list of object
        return instance


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, prog='database.py', description='''
Execute this module to create data_quality.db database and populate it with default list of values.
Example: python3 database.py

Execute this module with the following arguments to perform database operations:
- Name of the function you want to execute: create, read, update, delete
- Class name of the object on which you want to execute it: BatchOwner, DataSource, etc...
Example: python3 database.py create BatchOwner''')

    parser.add_argument('commands', nargs='*', type=str)
    arguments = parser.parse_args()
    arguments.commands

    # If no command line argument is supplied, create or repair database
    if len(arguments.commands) == 0:
        engine = create_engine('sqlite:///data_quality.db')

        # Create all tables in the engine
        log.info('Create database and tables')
        Base.metadata.create_all(engine)

        # Create database session to populate default list of values
        dbSession = sessionmaker(bind=engine)
        session = dbSession()

        # Insert default list of values
        with open('data_quality.dat', 'r') as dataFile:
            datadictionary = literal_eval(dataFile.read())
            for object in datadictionary['list_of_values']:
                    log.info('Insert default list of values for: {}'.format(object['class']))
                    for record in object['records']:
                        with Function(object['class']) as function:
                            function.create(**record)

    # If command line arguments are supplied execute corresponding functions
    elif len(arguments.commands) == 2:
        functionname = arguments.commands[0]
        classname = arguments.commands[1]
        with Function(classname) as function:
            instance = getattr(function, functionname)()

            # Print results if function is read
            if functionname == 'read':
                for item in instance:
                    record = utils.getobjectattributes(item)
                    print(json.dumps(record, indent=4, sort_keys=True))
    else:
        log.error('Invalid number of arguments, {} instead of 2'.format(len(arguments.commands)))
