"""Utility functions used by API scripts."""
import database
import utils


def create(resourcename, payload={}):
    """Generic create function called by post methods in apy.py."""
    with database.Function(resourcename) as function:
        record = function.create(**payload)
        print(record)

        # Convert database object into json
        response = utils.getobjectattributes(record)
    return(response)


def read(resourcename, payload={}):
    """Generic read function called by get methods in apy.py."""
    with database.Function(resourcename) as function:
        recordslist = function.read(**payload)

        # Convert database object into json
        response = []
        for record in recordslist:
            response.append(utils.getobjectattributes(record))
    return(response)


def update(resourcename, payload={}):
    """Generic update function called by put methods in apy.py."""
    with database.Function(resourcename) as function:
        record = function.update(**payload)

        # Convert database object into json
        response = utils.getobjectattributes(record)
    return (response)


def delete(resourcename, payload={}):
    """Generic update function called by put methods in apy.py."""
    with database.Function(resourcename) as function:
        function.delete(**payload)
    return ({})
