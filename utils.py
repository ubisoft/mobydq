"""Utility functions used by the data quality framework."""
from sqlalchemy import event, String, TypeDecorator
from sqlalchemy.engine import Engine
from sqlalchemy.ext import mutable
import json
import inspect
import logging
import re
import sys
import ntpath


def config_logger():
    """Load logging configuration."""
    logging.basicConfig(
        # filename='data_quality.log',
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapiconnection, connectionrecord):
    """Activate sqlite pragma to enforce foreign keys integrity, in particular for cascade delete."""
    cursor = dbapiconnection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_file_name(path):
    """Extract file name from absolute path."""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_object_attributes(object):
    """Get attributes and their values from the instance of a class and returns them as a dictionary."""
    attributes = inspect.getmembers(object, lambda a: not(inspect.isroutine(a)))
    dictionary = {}
    for attribute in attributes:
        # Exclude object attributes belonging to sqlachemy and database classes
        if not attribute[0].startswith('_') and not re.search("<class 'sqlalchemy*|<class 'database*", str(type(attribute[1]))):
                dictionary[attribute[0]] = str(attribute[1])
    return dictionary


class JsonEncodedDict(TypeDecorator):
    """Create sqlalchemy custom data type to enable json storage in event table."""

    impl = String

    def process_bind_param(self, value, dialect):
        """Dump."""
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        """Load."""
        return json.loads(value)
