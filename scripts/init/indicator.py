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

    def verify_indicator_parameters(self, authorization: str, indicator_type_id: int, parameters: List[dict]):
        """Verify if the list of indicator parameters is valid and return them as a dictionary."""

        # Build dictionary of parameter types referential
        query = 'query{allParameterTypes{nodes{id, name}}}'
        payload = {'query': query}
        response = utils.execute_graphql_request(authorization, payload)

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

    def get_data_frame(self, authorization: str, data_source: pandas.DataFrame, request: str, dimensions: str, measures: str):
        """Get data from data source. Return a formatted data frame according to dimensions and measures parameters."""

        # Get data source credentials
        query = 'query getDataSource($name: String!){dataSourceByName(name: $name){id, connectionString, login, dataSourceTypeId}}'
        variables = {'name': data_source}
        payload = {'query': query, 'variables': variables}
        response = utils.execute_graphql_request(authorization, payload)

        # Get connection object
        if response['data']['dataSourceByName']:
            data_source_id = response['data']['dataSourceByName']['id']
            data_source_type_id = response['data']['dataSourceByName']['dataSourceTypeId']
            connection_string = response['data']['dataSourceByName']['connectionString']
            login = response['data']['dataSourceByName']['login']

        # Get data source password
        data_source = DataSource()
        password = data_source.get_password(authorization, data_source_id)

        # Connect to data source
        log.info('Connect to data source.')
        connection = data_source.get_connection(data_source_type_id, connection_string, login, password)

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
        return eval(measure_value + alert_operator + alert_threshold) # pylint: disable=W0123

    def send_alert(self, indicator_id: int, indicator_name: str, session_id: int, distribution_list: List[str], alert_operator: str, alert_threshold: str, nb_records_alert: str, result_data: pandas.DataFrame):
        """Build the alert e-mail to be sent for the session."""

        # Create csv file to send in attachment
        file_name = f'indicator_{indicator_id}_session_{session_id}.csv'
        file_path = os.path.dirname(__file__) + "/" + file_name
        result_data.to_csv(file_path, header=True, index=False)

        # Prepare e-mail body
        body = {}
        body['indicator_name'] = indicator_name
        body['indicator_url'] = f'/indicators/{indicator_id}'
        body['session_log_url'] = f'/indicators/{indicator_id}/sessions/{session_id}/logs'
        body['alert_threshold'] = alert_operator + alert_threshold
        body['nb_records_alert'] = nb_records_alert

        # Send e-mail
        log.info('Send e-mail alert.')
        utils.send_mail(session_id, distribution_list, 'indicator', file_path, **body)
        os.remove(file_path)

        return True
