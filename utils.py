"""Utility functions used by the data quality framework."""
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
