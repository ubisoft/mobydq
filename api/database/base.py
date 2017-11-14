#!/usr/bin/env python
import logging
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base


log = logging.getLogger(__name__)


# Declarative base model to create database tables and classes
Base = declarative_base()


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(db_api_connection, connection_record):
    """Activate sqlite pragma to enforce foreign keys integrity, in particular for cascade delete."""
    cursor = db_api_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class DictHelper():
    def as_dict(self):
        result = {}
        for attr in self.__mapper__.columns.keys():
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            result[attr] = value
        return result
