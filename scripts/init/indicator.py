"""Manage class and methods for all types of indicators."""
from ast import literal_eval
from typing import List
import logging
import os
import pandas
from data_source import DataSource
from constants import IndicatorType
import utils

# Load logging configuration
log = logging.getLogger(__name__)


class Indicator:
    """Base class used to compute indicators, regardless of their type."""

    def verify_indicator_parameters(self, indicator_type_id: int, parameters: List[dict]):
        """Verify if the list of indicator parameters is valid and return them as a dictionary."""
        # Build dictionary of parameter types referential
        query = 'query{allParameterTypes{nodes{id,name}}}'
        response = utils.execute_graphql_request(query)
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
                missing_parameters.append(parameter_type)

        # Verify parameters specific to completeness and latency indicator types
        # Source, Source request
        if indicator_type_id in [IndicatorType.COMPLETENESS, IndicatorType.LATENCY]:
            for parameter_type_id in [6, 7]:
                if parameter_type_id not in indicator_parameters:
                    parameter_type = parameter_types_referential[parameter_type_id]
                    missing_parameters.append(parameter_type)

        if missing_parameters:
            missing_parameters = ', '.join(missing_parameters)
            error_message = f'Missing parameters: {missing_parameters}.'
            log.error(error_message)
            raise Exception(error_message)

        # Convert distribution list, dimensions and measures parameters to python list
        indicator_parameters[3] = literal_eval(indicator_parameters[3])  # Distribution list
        indicator_parameters[4] = literal_eval(indicator_parameters[4])  # Dimensions
        indicator_parameters[5] = literal_eval(indicator_parameters[5])  # Measures

        return indicator_parameters

    def get_data_frame(self, data_source: pandas.DataFrame, request: str, dimensions: str, measures: str):
        """Get data from data source. Return a formatted data frame according to dimensions and measures parameters."""
        # Get data source credentials
        query = '{dataSourceByName(name:"data_source"){id,connectionString,login,dataSourceTypeId}}'
        query = query.replace('data_source', data_source)
        response = utils.execute_graphql_request(query)

        # Get connection object
        if response['data']['dataSourceByName']:
            data_source_id = response['data']['dataSourceByName']['id']
            data_source_type_id = response['data']['dataSourceByName']['dataSourceTypeId']
            connection_string = response['data']['dataSourceByName']['connectionString']
            login = response['data']['dataSourceByName']['login']

        # Get data source password
        query = 'query{allDataSourcePasswords(condition:{id:data_source_id}){nodes{password}}}'
        query = query.replace('data_source_id', str(data_source_id))  # Use replace() instead of format() because of curly braces
        response = utils.execute_graphql_request(query)

        if response['data']['allDataSourcePasswords']['nodes'][0]:
            data_source = response['data']['allDataSourcePasswords']['nodes'][0]
            password = data_source['password']

            log.info('Connect to data source.')
            data_source = DataSource()
            connection = data_source.get_connection(data_source_type_id, connection_string, login, password)
        else:
            error_message = f'Data source {data_source} does not exist.'
            log.error(error_message)
            raise Exception(error_message)

        # Get data frame
        log.info('Execute request on data source.')
        data_frame = pandas.read_sql(request, connection)
        connection.close()

        if data_frame.empty:
            error_message = f'Request on data source {data_source} returned no data.'
            log.error(error_message)
            log.debug('Request: %s.', request)
            raise Exception(error_message)

        # Format data frame
        log.debug('Format data frame.')
        column_names = dimensions + measures
        data_frame.columns = column_names
        for column in dimensions:
            data_frame[column] = data_frame[column].astype(str)  # Convert dimension values to string

        return data_frame

    def is_alert(self, measure_value: str, alert_operator: str, alert_threshold: str):
        """
        Compare measure to alert threshold based on the alert operator.
        Return True if an alert must be sent, False otherwise.
        Supported alert operators are: ==, >, >=, <, <=, !=
        """
        return eval(str(measure_value) + alert_operator + str(alert_threshold)) # pylint: disable=W0123

    def compute_session_result(self, session_id: int, alert_operator: str, alert_threshold: str, result_data: pandas.DataFrame):
        """Compute aggregated results for the indicator session."""
        log.info('Compute session results.')
        nb_records = len(result_data)
        nb_records_alert = len(result_data.loc[result_data['Alert'] == True]) # pylint: disable=C0121
        nb_records_no_alert = len(result_data.loc[result_data['Alert'] == False]) # pylint: disable=C0121

        # Post results to database
        mutation = '''mutation{createSessionResult(input:{sessionResult:{
        alertOperator:"alert_operator",alertThreshold:alert_threshold,nbRecords:nb_records,
        nbRecordsAlert:nb_records_alert,nbRecordsNoAlert:nb_records_no_alert,userGroup:"test_group",sessionId:session_id}}){sessionResult{id}}}'''

        # Use replace() instead of format() because of curly braces
        mutation = mutation.replace('alert_operator', alert_operator)
        mutation = mutation.replace('alert_threshold', str(alert_threshold))
        mutation = mutation.replace('nb_records_no_alert', str(nb_records_no_alert))  # Order matters to avoid replacing other strings nb_records
        mutation = mutation.replace('nb_records_alert', str(nb_records_alert))  # Order matters to avoid replacing other strings nb_records
        mutation = mutation.replace('nb_records', str(nb_records))  # Order matters to avoid replacing other strings nb_records
        mutation = mutation.replace('session_id', str(session_id))
        utils.execute_graphql_request(mutation)

        return nb_records_alert

    def send_alert(self, indicator_id: int, indicator_name: str, session_id: int, distribution_list: List[str], alert_operator: str, alert_threshold: str, nb_records_alert: str, result_data: pandas.DataFrame):
        """Build the alert e-mail to be sent for the session."""
        # Create csv file to send in attachment
        file_name = f'indicator_{indicator_id}_session_{session_id}.csv'
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
        utils.send_mail(session_id, distribution_list, 'indicator', file_path, **body)
        os.remove(file_path)

        return True
