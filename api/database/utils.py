"""Utility functions for database operations."""
from cryptography.fernet import Fernet
import configparser
import logging
import os
import sys


def config_logger():
    """Load logging configuration."""
    logging.basicConfig(
        # filename='data_quality.log',
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_parameter(section, parameter_name=None):
    configuration = configparser.ConfigParser()
    configuration.read(os.path.dirname(__file__) + '/data_quality.cfg')
    if parameter_name:
        parameters = configuration[section][parameter_name]
    else:
        parameters = {}
        for key in configuration[section]:
            parameters[key] = configuration[section][key]
    return parameters


def encryption(action, value):
    secret_key = get_parameter('data_quality', 'secret_key')
    cipher = Fernet(secret_key.encode('utf-8'))
    if action == 'encrypt':
        value = cipher.encrypt(value.encode('utf-8'))
    elif action == 'decrypt':
        value = cipher.decrypt(value.encode('utf-8'))
    value = value.decode('utf-8')
    return value
