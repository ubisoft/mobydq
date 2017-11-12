"""Utility functions used by API scripts."""
import inspect
import os
import sys

# Modify python path to allow import module from parent folder
current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_directory = os.path.dirname(current_directory)
sys.path.insert(0, parent_directory)

from database import DbOperation
import batch
import utils


def create(resource_name, payload=None):
    """Generic create function called by post methods in api.py."""
    if not payload:
        payload = {}

    record = DbOperation(resource_name).create(**payload)

    # Convert database object into json
    response = utils.get_object_attributes(record)
    return(response)


def read(resource_name, payload=None):
    """Generic read function called by get methods in api.py."""
    if not payload:
        payload = {}

    record_list = DbOperation(resource_name).read(**payload)

    # Convert database object into json
    response = []
    for record in record_list:
        response.append(utils.get_object_attributes(record))
    return(response)


def update(resource_name, payload=None):
    """Generic update function called by put methods in api.py."""
    if not payload:
        payload = {}

    record = DbOperation(resource_name).update(**payload)

    # Convert database object into json
    response = utils.get_object_attributes(record)
    return (response)


def delete(resource_name, payload=None):
    """Generic update function called by put methods in api.py."""
    if not payload:
        payload = {}

    DbOperation(resource_name).delete(**payload)
    return ({})


def log_batch(batch_owner_id, event):
    """Manage batch status for the corresponding batch owner."""
    batch_list = batch.log_batch(batch_owner_id, event)
    if batch_list:
        response = {'message': 'Batch status updated.'}
    else:
        response = {'message': 'Batch status was not updated due to invalid event.'}
    return (response)
