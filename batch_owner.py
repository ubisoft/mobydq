"""Manage batch owners."""
import argparse
import database
import logging
import utils


# Load logger
utils.configlogger()
log = logging.getLogger(__name__)


def create():
    """Create batch owner."""
    name = input('Enter new batch owner name: ')
    with database.DatabaseFunction('BatchOwner') as function:
        function.create(name=name)
    return True


def read():
    """Get batch owner."""
    name = input('Enter batch owner name to be selected: ')
    with database.DatabaseFunction('BatchOwner') as function:
        batchownerlist = function.read(name=name)
        for attribute in dir(batchownerlist[0]):
            if not attribute.startswith('_') and attribute != 'metadata' and getattr(batchownerlist[0], attribute) != []:
                print(attribute + ': ' + str(getattr(batchownerlist[0], attribute)))
    return True


def update():
    """Update batch owner."""
    with database.DatabaseFunction('BatchOwner') as function:
        batchownerlist = function.update()
    return True


def delete():
    """Delete batch owner."""
    with database.DatabaseFunction('BatchOwner') as function:
        batchownerlist = function.delete()
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-function',
        dest='function',
        type=str,
        help='Enter the name of the function you want to performe on batch owners.',
        choices=['create', 'read', 'update', 'delete'])
    arguments = parser.parse_args()
    arguments.function

    # Call function to perform operation on batch owner
    if arguments.function == 'create' or arguments.function is None:
        create()

    elif arguments.function == 'read':
        read()

    elif arguments.function == 'update':
        update()

    elif arguments.function == 'delete':
        delete()

    else:
        log.error('Invalid argument function: {}'.format(arguments.function))
