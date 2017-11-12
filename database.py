#!/usr/bin/env python
"""Setup data quality framework database and perform CRUD operations."""
from ast import literal_eval
from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, TypeDecorator
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
import json
import logging
import os
import sys
import utils

# Load logger
utils.config_logger()
log = logging.getLogger(__name__)

# Declarative base model to create database tables and classes
Base = declarative_base()


class DictHelper():
    def as_dict(self):
        result = {}
        for attr in self.__mapper__.columns.keys():
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            result[attr] = value
        return result


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(db_api_connection, connection_record):
    """Activate sqlite pragma to enforce foreign keys integrity, in particular for cascade delete."""
    cursor = db_api_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class JsonEncodedDict(TypeDecorator):
    """Create sqlalchemy custom data type to enable json storage in event table."""

    impl = String

    def process_bind_param(self, value, dialect):
        """Dump."""
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        """Load."""
        return json.loads(value)


class Status(Base, DictHelper):
    """Status for batches and sessions."""

    __tablename__ = 'status'

    id = Column('status_id', Integer, primary_key=True)
    name = Column('status', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    batch = relationship('Batch', backref='Status')
    session = relationship('Session', backref='Status')


class DataSourceType(Base, DictHelper):
    """Types of data sources."""

    __tablename__ = 'data_source_type'

    id = Column('data_source_type_id', Integer, primary_key=True)
    name = Column('data_source_type', String, nullable=False, unique=True)
    type = Column('data_source_parent_type', String, nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    dataSource = relationship('DataSource', backref='DataSourceType')


class DataSource(Base, DictHelper):
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


class BatchOwner(Base, DictHelper):
    """Batch owners."""

    __tablename__ = 'batch_owner'

    id = Column('batch_owner_id', Integer, primary_key=True)
    name = Column('batch_owner', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    batch = relationship('Batch', backref='BatchOwner', passive_deletes=True)
    indicator = relationship('Indicator', backref='BatchOwner')


class Batch(Base, DictHelper):
    """Batches."""

    __tablename__ = 'batch'

    id = Column('batch_id', Integer, primary_key=True)
    batchOwnerId = Column('batch_owner_id', Integer, ForeignKey('batch_owner.batch_owner_id', ondelete='CASCADE'), nullable=False)
    statusId = Column('status_id', Integer, ForeignKey('status.status_id'), nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    session = relationship('Session', backref='Batch', passive_deletes=True)


class IndicatorType(Base, DictHelper):
    """Types of indicators."""

    __tablename__ = 'indicator_type'

    id = Column('indicator_type_id', Integer, primary_key=True)
    name = Column('indicator_type', String, nullable=False, unique=True)
    module = Column('module', String, nullable=False)
    function = Column('function', String, nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    indicator = relationship('Indicator', backref='IndicatorType')


class Indicator(Base, DictHelper):
    """Data quality indicators."""

    __tablename__ = 'indicator'

    id = Column('indicator_id', Integer, primary_key=True)
    name = Column('indicator', String, nullable=False, unique=True)
    description = Column('indicator_description', String, nullable=False)
    indicatorTypeId = Column('indicator_type_id', Integer, ForeignKey('indicator_type.indicator_type_id'), nullable=False)
    batchOwnerId = Column('batch_owner_id', Integer, ForeignKey('batch_owner.batch_owner_id'), nullable=False)
    executionOrder = Column('execution_order', Integer, nullable=False, default=0)
    # alertOperator = Column('alert_operator', String, nullable=False) # This got moved to indicator parameters
    # alertThreshold = Column('alert_threshold', Float, nullable=False) # This got moved to indicator parameters
    # distributionList = Column('distribution_list', String, nullable=False) # This got moved to indicator parameters
    active = Column('flag_active', Boolean, nullable=False, default=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    indicatorParameter = relationship('IndicatorParameter', backref='Indicator', passive_deletes=True)
    indicatorResult = relationship('IndicatorResult', backref='Indicator', passive_deletes=True)
    session = relationship('Session', backref='Indicator', passive_deletes=True)


class IndicatorParameter(Base, DictHelper):
    """Indicator parameters."""

    __tablename__ = 'indicator_parameter'

    id = Column('indicator_parameter_id', Integer, primary_key=True)
    name = Column('indicator_parameter', String, nullable=False)
    value = Column('indicator_parameter_value', String, nullable=False)
    indicatorId = Column('indicator_id', Integer, ForeignKey('indicator.indicator_id', ondelete='CASCADE'), nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())


class Session(Base, DictHelper):
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


class EventType(Base, DictHelper):
    """Types of events."""

    __tablename__ = 'event_type'

    id = Column('event_type_id', Integer, primary_key=True)
    name = Column('event_type', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    event = relationship('Event', backref='EventType')


class Event(Base, DictHelper):
    """Events."""

    __tablename__ = 'event'

    id = Column('event_id', Integer, primary_key=True)
    eventTypeId = Column('event_type_id', Integer, ForeignKey('event_type.event_type_id'), nullable=False)
    sessionId = Column('session_id', Integer, ForeignKey('session.session_id', ondelete='CASCADE'), nullable=False)
    content = Column('content', JsonEncodedDict)
    createdDate = Column('created_date', DateTime, server_default=func.now())


class IndicatorResult(Base, DictHelper):
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
    # This cannot be used for indicators with multiple measures
    # avgResult = Column('avg_result', Float, nullable=False)
    # This cannot be used for indicators with multiple measures
    # avgResultAlert = Column('avg_result_alert', Float, nullable=False)
    # This cannot be used for indicators with multiple measures
    # avgResultNoAlert = Column('avg_result_no_alert', Float, nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())


class DbOperation:
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

    def _create(self, session, **kwargs):
        """
        Create record. Return list of objects.
        A session need to be provided
        """
        # Verify record does not exist
        instance = session.query(self.object).filter_by(**kwargs).first()
        if instance:
            log.error('{} already exists with values: {}'.format(self.object.__name__, kwargs))
        else:
            instance = self.object(**kwargs)
            session.add(instance)
            session.commit()
            log.info('{} created with values: {}'.format(self.object.__name__, kwargs))

        # Return object
        instance = session.query(self.object).filter_by(**kwargs).first()
        return instance

    def create(self, **kwargs):
        """Create record. Return list of objects."""
        with self.open_session() as session:
            return self._create(session, **kwargs)

    def _read(self, session, **kwargs):
        """
        Get record or list of records. Return list of objects.
        A session need to be provided
        """
        instance = session.query(self.object).filter_by(**kwargs).all()
        log.info('Select {} returned {} records'.format(self.object.__name__, len(instance)))
        # Return list of objects
        return instance

    def read(self, **kwargs):
        """Get record or list of records. Return list of objects."""
        with self.open_session() as session:
            return self._read(session, **kwargs)

    def _update(self, session, **kwargs):
        """
        Update record. Return list of objects.
        A session need to be provided
        """
        # Verify record exists
        instance = session.query(self.object).filter_by(id=kwargs['id']).first()
        if not instance:
            log.error('No {} found with Id: {}'.format(self.object.__name__, kwargs['id']))
        else:
            instance = session.query(self.object).filter_by(id=kwargs['id']).update(kwargs)
            session.commit()
            log.info('{} with Id {} updated'.format(self.object.__name__, kwargs['id']))

        # Return object
        instance = session.query(self.object).filter_by(**kwargs).first()
        return instance

    def update(self, **kwargs):
        """Update record. Return list of objects."""
        with self.open_session() as session:
            return self._update(session, **kwargs)

    def _delete(self, session, **kwargs):
        """
        Delete record. Return empty list of objects.
        A session need to be provided
        """
        # Verify record exists
        instance = session.query(self.object).filter_by(**kwargs).first()
        if not instance:
            # FIXME An exception raised would probably be better. Handling to be done by the caller
            log.error('No {} found with values: {}'.format(self.object.__name__, kwargs))
        else:
            instance = session.query(self.object).filter_by(**kwargs).delete()
            session.commit()
            log.info('{} with values {} deleted'.format(self.object.__name__, kwargs))

        # Return empty object
        return instance

    def delete(self, **kwargs):
        """Delete record. Return empty list of objects."""
        # Verify record exists
        with self.open_session() as session:
            return self._delete(session, **kwargs)


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
