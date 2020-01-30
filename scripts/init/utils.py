"""Utility methods."""
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
import configparser
import json
import logging
import os
import requests
import smtplib
import traceback


# Load logging configuration
log = logging.getLogger(__name__)


class CustomLogHandler(logging.Handler):
    """Custom log handler to send log messages to GraphQL API."""

    def __init__(self, authorization: str, batch_id: int = None, session_id: int = None, data_source_id: int = None):
        logging.Handler.__init__(self)
        self.authorization = authorization
        self.batch_id = batch_id
        self.session_id = session_id
        self.data_source_id = data_source_id

    def emit(self, record):
        file_name = record.name
        log_level = record.levelname
        log_message = json.dumps(record.message)  # Sanitize log message for http request

        # Build mutation payload
        mutation = 'mutation{createLog(input:{log:{fileName:"file_name",logLevel:"log_level",message:log_message foreign_keys}}){log{id}}}'
        mutation = mutation.replace('file_name', file_name)  # Use replace() instead of format() because of curly braces
        mutation = mutation.replace('log_level', log_level)  # Use replace() instead of format() because of curly braces
        mutation = mutation.replace('log_message', log_message)  # Use replace() instead of format() because of curly braces

        # Add foreign keys to log record
        foreign_keys = ''
        if self.batch_id != None:
            foreign_keys = ',batchId:{}'.format(self.batch_id)
        if self.session_id != None:
            foreign_keys = foreign_keys + ',sessionId:{}'.format(self.session_id)
        if self.data_source_id != None:
            foreign_keys = foreign_keys + ',dataSourceId:{}'.format(self.data_source_id)

        mutation = mutation.replace('foreign_keys', foreign_keys)  # Use replace() instead of format() because of curly braces
        mutation = {'query': mutation}  # Convert to dictionary
        execute_graphql_request(self.authorization, mutation)

def get_parameter(section: str, parameter_name: str = None):
    """Get parameters from flat file config.cfg."""
    configuration = configparser.ConfigParser()
    path = os.path.dirname(__file__)
    configuration.read(path + '/scripts.cfg')
    if parameter_name:
        parameters = configuration[section][parameter_name]
    else:
        parameters = {}
        for key in configuration[section]:
            parameters[key] = configuration[section][key]

    return parameters

def execute_graphql_request(authorization: str, payload: dict):
    """Method to execute http request on the GraphQL API."""

    url = 'http://graphql:5433/graphql'  # url = get_parameter('graphql', 'url')
    headers = {'Content-Type': 'application/json'}
    if authorization:
        headers['Authorization'] = authorization
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    return data

def send_mail(session_id: int, distribution_list: list, template: str = None, attachment: any = None, **kwargs):
    """Send e-mail to the distribution list."""
    # Verify e-mail configuration
    config = get_parameter('mail')
    for key, value in config.items():
        if value in ['change_me', '', None]:
            error_message = f'Cannot send e-mail notification due to invalid configuration for mail parameter {key}.'
            log.error(error_message)
            raise Exception(error_message)

    # Construct e-mail header
    email = MIMEMultipart()
    email['From'] = config['sender']
    email['To'] = ', '.join(distribution_list)

    # Construct e-mail body and update body template
    if template == 'indicator':
        indicator_name = kwargs['indicator_name']
        email['Subject'] = f'Data quality alert: {indicator_name}'
        html = open(os.path.dirname(__file__) + f'/email/{template}.html', 'r')
        body = html.read()
        body = Template(body)
        body = body.render(**kwargs)

    elif template == 'error':
        indicator_name = kwargs['indicator_name']
        email['Subject'] = f'Data quality error: {indicator_name}'
        html = open(os.path.dirname(__file__) + f'/email/{template}.html', 'r')
        body = html.read()
        body = Template(body)
        kwargs['session_id'] = session_id
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
    if attachment:
        attachment_path = os.path.join(os.path.dirname(__file__), attachment)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment_path, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
        email.attach(part)

    # Connect to smtp server
    connection = smtplib.SMTP(config['host'], config['port'])

    # If smtp server is Gmail activate encryption and authenticate user
    if config['host'] == 'smtp.gmail.com':
        connection.ehlo()
        connection.starttls()
        connection.login(config['sender'], config['password'])

    # Send email
    try:
        connection.sendmail(email['From'], email['To'], email.as_string())

    except Exception: # pylint: disable=broad-except
        error_message = traceback.format_exc()
        log.error(error_message)

    connection.quit()

    return True

def send_error(indicator_id: int, indicator_name: str, session_id: int, distribution_list: list, error_message: str):
    """Build the error e-mail to be sent for the session."""
    # Prepare e-mail body
    body = {}
    body['indicator_id'] = indicator_id
    body['indicator_name'] = indicator_name
    body['error_message'] = error_message

    # Send e-mail
    log.info('Send error e-mail.')
    send_mail(session_id, distribution_list, 'error', None, **body)

    return True
