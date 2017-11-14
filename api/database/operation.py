import logging
import os
import sys
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base
from .db_utils import encryption

from .batch import BatchOwner, Batch
from .data_source import DataSource, DataSourceType
from .event import Event, EventType
from .indicator import Indicator, IndicatorType, IndicatorParameter
from .session import Session
from .status import Status

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
            # Apply encryption on password fields
            for key in kwargs:
                if key == 'password' and kwargs[key] != '':
                    kwargs[key] = encryption('encrypt', kwargs[key])

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
