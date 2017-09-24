import jinja2
import logging
import sys


def updateQuery(query, parameters):
    """Update an SQL query template, replacing {{place_holders}} by the values provided in the parameters dictionrary"""
    template = jinja2.Template(query)
    query = template.render(parameters)
    return(query)


def configLogger():
    """Load logging configuration"""
    logging.basicConfig(
        # filename='data_quality.log',
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def dictionary(cursor, row):
    """Converts SQLite cursor to dictionary"""
    dictionary = {}
    for index, column in enumerate(cursor.description):
        dictionary[column[0]] = row[index]
    return dictionary
