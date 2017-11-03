"""Utility functions used by API scripts."""
import inspect
import os
import sys

# Modify python path to allow import module from parent folder
current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_directory = os.path.dirname(current_directory)
sys.path.insert(0, parent_directory)

from database import DbOperation
import utils


def create(resource_name, payload={}):
    """Generic create function called by post methods in apy.py."""
    with DbOperation(resource_name) as op:
        record = op.create(**payload)

        # Convert database object into json
        response = utils.get_object_attributes(record)
    return(response)


def read(resource_name, payload={}):
    """Generic read function called by get methods in apy.py."""
    with DbOperation(resource_name) as op:
        record_list = op.read(**payload)

        # Convert database object into json
        response = []
        for record in record_list:
            response.append(utils.get_object_attributes(record))
    return(response)


def update(resource_name, payload={}):
    """Generic update function called by put methods in apy.py."""
    with DbOperation(resource_name) as op:
        record = op.update(**payload)

        # Convert database object into json
        response = utils.get_object_attributes(record)
    return (response)


def delete(resource_name, payload={}):
    """Generic update function called by put methods in apy.py."""
    with DbOperation(resource_name) as op:
        op.delete(**payload)
    return ({})
