#!/usr/bin/env python
"""Utility functions used by API scripts."""
from database.operation import Operation
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from graphql_relay.node.node import from_global_id
from jinja2 import Template
import configparser
import inspect
import logging
import os
import smtplib
import sys

# Load logging configuration
log = logging.getLogger(__name__)


def init():
    """Modify python path to allow module import from api folder."""
    api_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    sys.path.insert(0, api_directory)
    sys.path.insert(0, api_directory + '/database')


def get_parameter(section, parameter_name=None):
    """Get parameters from flat file api.cfg."""
    configuration = configparser.ConfigParser()
    path = os.path.dirname(__file__)
    configuration.read(path + '/api.cfg')
    if parameter_name:
        parameters = configuration[section][parameter_name]
    else:
        parameters = {}
        for key in configuration[section]:
            parameters[key] = configuration[section][key]
    return parameters


def input_to_dictionary(input):
    """Convert GraphQL mutation inputs into a dictionary object."""
    data = {}
    for key in input:
        if key[-2:].lower() == 'id':
            input[key] = from_global_id(input[key])[1]  # Convert GraphQL global id to database id
        data[key] = input[key]
    return data


def send_mail(template, distribution_list, attachment=None, **kwargs):
    # Get e-mail configuration
    config = get_parameter('mail')
    for key, value in config.items():
        if value in ['change_me', '', None]:
            log.info('Cannot send e-mail notification due to invalid configuration for mail parameter {}: {}'.format(key, value))
            return False

    # Construct e-mail header
    email = MIMEMultipart()
    email['From'] = config['sender']
    email['To'] = ', '.join(distribution_list)

    # Construct e-mail body and update body template
    if template == 'indicator':
        email['Subject'] = 'Data quality alert: {}'.format(kwargs['indicator_name'])
        html = open(os.path.dirname(__file__) + '/email/{}.html'.format(template), 'r')
        body = html.read()
        body = Template(body)
        body = body.render(**kwargs)

    elif template == 'error':
        email['Subject'] = 'Data quality error: {}'.format(kwargs['indicator_name'])
        html = open(os.path.dirname(__file__) + '/email/{}.html'.format(template), 'r')
        body = html.read()
        body = Template(body)
        body = body.render(**kwargs)

    else:
        email['Subject'] = 'Data quality notification'
        html = open(os.path.dirname(__file__) + '/email/default.html', 'r')
        body = html.read()
        body = Template(body)
        body = body.render(**kwargs)

    # Attache body to e-mail
    body = MIMEText(body, 'html')
    email.attach(body)

    # Add attachment to e-mail
    if attachment is not None:
        attachment_path = os.path.join(os.path.dirname(__file__), attachment)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment_path, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(attachment_path)))
        email.attach(part)

    # Send e-mail via smtp server
    connexion = smtplib.SMTP(config['host'], config['port'])
    connexion.sendmail(config['sender'], distribution_list, email.as_string())
    connexion.quit()
    return True
