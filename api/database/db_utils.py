import configparser
import logging
import os
from cryptography.fernet import Fernet

log = logging.getLogger(__name__)


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
