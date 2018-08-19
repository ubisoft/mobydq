from ast import literal_eval
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
import configparser
import logging
import os
import pyodbc
import requests
import smtplib
import sqlite3

# Load logging configuration
log = logging.getLogger(__name__)


def get_parameter(section, parameter_name=None):
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


def execute_graphql_request(payload):
    """Execute queries and mutations on the GraphQL API."""
    url = 'http://graphql:5433/graphql'  # Should be moved to config file
    headers = {'Content-Type': 'application/graphql'}
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    return data


def update_batch_status(batch_id, batch_status):
    """Update a batch status."""
    mutation = '''mutation{updateBatchById(input:{id:batch_id,batchPatch:{status:"batch_status"}}){batch{status}}}'''
    mutation = mutation.replace('batch_id', str(batch_id))  # Use replace() instead of format() because of curly braces
    mutation = mutation.replace('batch_status', str(batch_status))  # Use replace() instead of format() because of curly braces
    data = execute_graphql_request(mutation)
    return data


def update_session_status(session_id, session_status):
    """Update a session status."""
    mutation = '''mutation{updateSessionById(input:{id:session_id,sessionPatch:{status:"session_status"}}){session{status}}}'''
    mutation = mutation.replace('session_id', str(session_id))  # Use replace() instead of format() because of curly braces
    mutation = mutation.replace('session_status', str(session_status))  # Use replace() instead of format() because of curly braces
    data = execute_graphql_request(mutation)
    return data


def verify_indicator_parameters(self, indicator_type_id, parameters):
    """Verify if the list of indicator parameters is valid and return them as a dictionary."""
    # Build dictionary of parameter types referential
    query = '''query{allParameterTypes{nodes{id,name}}}'''
    response = execute_graphql_request(query)
    parameter_types_referential = {}
    for parameter_type in response['data']['allParameterTypes']['nodes']:
        parameter_types_referential[parameter_type['id']] = parameter_type['name']

    # Build dictionary of indicator parameters
    indicator_parameters = {}
    for parameter in parameters:
        indicator_parameters[parameter['parameterTypeId']] = parameter['value']

    # Verify mandatory parameters exist
    # Alert operator, Alert threshold, Distribution list, Dimensions, Measures, Target, Target request
    missing_parameters = []
    for parameter_type_id in [1, 2, 3, 4, 5, 8, 9]:
        if parameter_type_id not in indicator_parameters:
            parameter_type = parameter_types_referential[parameter_type_id]
            missing_parameters.append[parameter_type]

    # Verify parameters specific to completeness and latency indicator types
    # Source, Source request
    if indicator_type_id in [1, 3]:
        for parameter_type_id in [6, 7]:
            if parameter_type_id not in indicator_parameters:
                parameter_type = parameter_types_referential[parameter_type_id]
                missing_parameters.append[parameter_type]

    if missing_parameters:
        missing_parameters = ', '.join(missing_parameters)
        log.error('Missing parameters: {missing_parameters}.'.format(missing_parameters))
        # Raise alert, send e-mail

    # Convert distribution list, dimensions and measures parameters to python list
    indicator_parameters[3] = literal_eval(indicator_parameters[3])  # Distribution list
    indicator_parameters[4] = literal_eval(indicator_parameters[4])  # Dimensions
    indicator_parameters[5] = literal_eval(indicator_parameters[5])  # Measures

    return indicator_parameters


def send_mail(distribution_list, template=None, attachment=None, **kwargs):
    """Send e-mail to the distribution list."""
    # Verify e-mail configuration
    config = get_parameter('mail')
    for key, value in config.items():
        if value in ['change_me', '', None]:
            log.error('Cannot send e-mail notification due to invalid configuration for mail parameter {key}.'.format(key=key))
            # Raise alert

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
    if attachment:
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


def get_connection(self, data_source_type_id, connection_string, login=None, password=None):
    """Connect to a data source. Return a connection object."""
    # Add login to connection string if it is not empty
    if login:
        connection_string = connection_string + 'uid={login};'.format(login=login)

    # Add password to connection string if it is not empty
    if password:
        connection_string = connection_string + 'pwd={password};'.format(password=password)

    # Hive
    if data_source_type_id == 1:
        connection = pyodbc.connect(connection_string)
        connection.setencoding(encoding='utf-8')

    # Impala
    elif data_source_type_id == 2:
        connection = pyodbc.connect(connection_string)
        connection.setencoding(encoding='utf-8')

    # MariaDB
    elif data_source_type_id == 3:
        connection = pyodbc.connect(connection_string)

    # Microsoft SQL Server
    elif data_source_type_id == 4:
        connection = pyodbc.connect(connection_string)

    # MySQL
    elif data_source_type_id == 5:
        connection = pyodbc.connect(connection_string)

    # Oracle
    elif data_source_type_id == 6:
        connection = pyodbc.connect(connection_string)

    # PostgreSQL
    elif data_source_type_id == 7:
        connection = pyodbc.connect(connection_string)
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setencoding(encoding='utf-8')

    # SQLite
    elif data_source_type_id == 8:
        connection = sqlite3.connect(connection_string)

    # Teradata
    elif data_source_type_id == 9:
        connection = pyodbc.connect(connection_string)
        connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
        connection.setencoding(encoding='utf-8')

    return connection
