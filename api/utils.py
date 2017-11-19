"""Utility functions used by API scripts."""
from database.operation import Operation


def create(resource_name, payload=None):
    """Generic create function called by post methods in api.py."""
    if not payload:
        payload = {}

    record = Operation(resource_name).create(**payload)

    # Convert database object into json
    response = record.as_dict()
    return(response)


def read(resource_name, payload=None):
    """Generic read function called by get methods in api.py."""
    if not payload:
        payload = {}

    record_list = Operation(resource_name).read(**payload)

    # Convert database object into json
    response = []
    for record in record_list:
        response.append(record.as_dict())
    return(response)


def update(resource_name, payload=None):
    """Generic update function called by put methods in api.py."""
    if not payload:
        payload = {}

    record = Operation(resource_name).update(**payload)

    # Convert database object into json
    response = record.as_dict()
    return (response)


def delete(resource_name, payload=None):
    """Generic update function called by put methods in api.py."""
    if not payload:
        payload = {}

    Operation(resource_name).delete(**payload)
    return ({})
