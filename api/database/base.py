#!/usr/bin/env python
"""Database configuration."""
from datetime import datetime
from sqlalchemy import create_engine, event
from sqlalchemy import String, TypeDecorator
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import json
import os

# Create database engine used by graphql
db_path = os.path.join(os.path.dirname(__file__), 'data_quality.db')
db_uri = 'sqlite:///{}'.format(db_path)
engine = create_engine(db_uri, convert_unicode=True)
dbSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Declarative base model to create database tables and classes
Base = declarative_base()
Base.query = dbSession.query_property()  # Used by graphql to execute queries


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(db_api_connection, connection_record):
    """Activate sqlite pragma to enforce foreign keys integrity, in particular for cascade delete."""
    cursor = db_api_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Json(TypeDecorator):
    """Create sqlalchemy custom data type to enable json storage in event table."""
    impl = String

    def process_bind_param(self, value, dialect):
        """Dump."""
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        """Load."""
        return json.loads(value)


class Dictionary():
    """Convert instance of a class to a dictionary."""
    def as_dict(self):
        result = {}
        for attribute in self.__mapper__.columns.keys():
            value = getattr(self, attribute)
            if isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            result[attribute] = value
        return result
