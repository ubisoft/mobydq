"""Utility functions used by the data quality framework."""
import inspect
import logging
import sys
import ntpath


def configlogger():
    """Load logging configuration."""
    logging.basicConfig(
        # filename='data_quality.log',
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def getfilename(path):
    """Extract file name from absolute path."""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def getobjectattributes(object):
    """Get attributes and their values from the instance of a class and returns them as a dictionary."""
    attributes = inspect.getmembers(object, lambda a: not(inspect.isroutine(a)))
    dictionary = {}
    for attribute in attributes:
        if not attribute[0].startswith('_') and attribute[1] != [] and attribute[0] != 'metadata':
            dictionary[attribute[0]] = str(attribute[1])
    return dictionary
