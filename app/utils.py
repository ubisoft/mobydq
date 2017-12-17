#!/usr/bin/env python
"""Functions to perform database operations."""
import configparser
import logging
import os

# Load logging configuration
log = logging.getLogger(__name__)


def get_parameter(section, parameter_name=None):
    configuration = configparser.ConfigParser()
    path = os.path.dirname(__file__)
    configuration.read(path + '/app.cfg')
    if parameter_name:
        parameters = configuration[section][parameter_name]
    else:
        parameters = {}
        for key in configuration[section]:
            parameters[key] = configuration[section][key]
    return parameters
