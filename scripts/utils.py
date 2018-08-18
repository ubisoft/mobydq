from ast import literal_eval
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
import configparser
import logging
import os
import pandas
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


def verify_indicator_parameters(indicator_type_id, parameters):
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


def get_connection(data_source_type_id, connection_string, login=None, password=None):
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


def get_data_frame(data_source, request, dimensions, measures):
    """Get data from data source. Return a formatted data frame according to dimensions and measures parameters."""
    # Get data source credentials
    query = '''{dataSourceByName(name:"data_source"){connectionString,login,password,dataSourceTypeId}}'''
    query = query.replace('data_source', data_source)
    response = execute_graphql_request(query)

    if response['data']['dataSourceByName']:
        # Get connection object
        data_source_type_id = response['data']['dataSourceByName']['dataSourceTypeId']
        connection_string = response['data']['dataSourceByName']['connectionString']
        login = response['data']['dataSourceByName']['login']
        password = response['data']['dataSourceByName']['password']
        log.info('Connect to data source {data_source}.'.format(data_source=data_source))
        connection = get_connection(data_source_type_id, connection_string, login, password)
    else:
        log.error('Data source {data_source} does not exist.'.format(data_source=data_source))
        # Raise alert, send e-mail

    # Get data frame
    log.info('Execute request on data source.'.format(data_source=data_source))
    data_frame = pandas.read_sql(request, connection)
    if data_frame.empty:
        log.error('Request on data source {data_source} returned no data.'.format(data_source=data_source))
        log.debug('Request: {request}.'.format(request=request))
        # Raise alert, send e-mail

    # Format data frame
    log.debug('Format data frame.')
    column_names = dimensions + measures
    data_frame.columns = column_names
    for column in dimensions:
        data_frame[column] = data_frame[column].astype(str)  # Convert dimension values to string

    return data_frame


def is_alert(measure_value, alert_operator, alert_threshold):
    """
    Compare measure to alert threshold based on the alert operator.
    Return True if an alert must be sent, False otherwise.
    Supported alert operators are: ==, >, >=, <, <=, !=
    """
    if eval(str(measure_value) + alert_operator + str(alert_threshold)):
        return True
    else:
        return False


def compute_session_result(session_id, alert_operator, alert_threshold, result_data):
    """Compute aggregated results for the indicator session."""
    nb_records = len(result_data)
    nb_records_alert = len(result_data.loc[result_data['Alert'] == True])
    nb_records_no_alert = len(result_data.loc[result_data['Alert'] == False])

    # Post results to database
    mutation = '''mutation{createSessionResult(input:{sessionResult:{
    alertOperator:"alert_operator",alertThreshold:alert_threshold,nbRecords:nb_records,
    nbRecordsAlert:nb_records_alert,nbRecordsNoAlert:nb_records_no_alert,sessionId:session_id}}){sessionResult{id}}}'''

    # Use replace() instead of format() because of curly braces
    mutation = mutation.replace('alert_operator', alert_operator)
    mutation = mutation.replace('alert_threshold', str(alert_threshold))
    mutation = mutation.replace('nb_records_no_alert', str(nb_records_no_alert))  # Order matters to avoid replacing other strings nb_records
    mutation = mutation.replace('nb_records_alert', str(nb_records_alert))  # Order matters to avoid replacing other strings nb_records
    mutation = mutation.replace('nb_records', str(nb_records))  # Order matters to avoid replacing other strings nb_records
    mutation = mutation.replace('session_id', str(session_id))
    execute_graphql_request(mutation)

    return nb_records_alert


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


def send_alert(indicator_id, indicator_name, session_id, distribution_list, alert_operator, alert_threshold, nb_records_alert, result_data):
    """Build the alert e-mail to be sent for the session."""
    # Create csv file to send in attachment
    file_name = 'indicator_{indicator_id}_session_{session_id}.csv'.format(indicator_id=indicator_id, session_id=session_id)
    file_path = os.path.dirname(__file__) + "/" + file_name
    result_data.to_csv(file_path, header=True, index=False)

    # Prepare e-mail body
    body = {}
    body['indicator_name'] = indicator_name
    body['alert_threshold'] = alert_operator + alert_threshold
    body['nb_records_alert'] = nb_records_alert
    body['log_url'] = 'http://'  # To be updated

    # Send e-mail
    log.info('Send e-mail alert.')
    send_mail(distribution_list, 'indicator', file_path, **body)
    os.remove(file_path)

    return True
