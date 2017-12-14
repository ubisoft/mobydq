#!/usr/bin/env python
"""Utility functions used by API scripts."""
from api.database.operation import Operation
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
import logging
import os
import smtplib

# Load logging configuration
log = logging.getLogger(__name__)


def create(resource_name, payload=None):
    """Generic create function called by post methods in api.py."""
    if not payload:
        payload = {}

    record = Operation(resource_name).create(**payload)

    # Convert database object into json
    response = record.as_dict()
    return response


def read(resource_name, payload=None):
    """Generic read function called by get methods in api.py."""
    if not payload:
        payload = {}

    record_list = Operation(resource_name).read(**payload)

    # Convert database object into json
    response = []
    for record in record_list:
        response.append(record.as_dict())
    return response


def update(resource_name, payload=None):
    """Generic update function called by put methods in api.py."""
    if not payload:
        payload = {}

    record = Operation(resource_name).update(**payload)

    # Convert database object into json
    response = record.as_dict()
    return response


def delete(resource_name, payload=None):
    """Generic update function called by put methods in api.py."""
    if not payload:
        payload = {}

    Operation(resource_name).delete(**payload)
    return {'message': 'Record deleted successfully'}


def send_mail(template, distribution_list, attachment=None, **kwargs):
    # Get e-mail configuration
    config = Operation.get_parameter('mail')
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
