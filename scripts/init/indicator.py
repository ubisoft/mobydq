import logging
import os
import pandas
import utils

# Load logging configuration
log = logging.getLogger(__name__)


class Indicator:
    """Base class used to compute indicators, regardless of their type."""

    def __init__(self):
        pass

    def get_data_frame(self, data_source, request, dimensions, measures):
        """Get data from data source. Return a formatted data frame according to dimensions and measures parameters."""
        # Get data source credentials
        query = '''{dataSourceByName(name:"data_source"){connectionString,login,password,dataSourceTypeId}}'''
        query = query.replace('data_source', data_source)
        response = utils.execute_graphql_request(query)

        # Get connection object
        if response['data']['dataSourceByName']:
            data_source_type_id = response['data']['dataSourceByName']['dataSourceTypeId']
            connection_string = response['data']['dataSourceByName']['connectionString']
            login = response['data']['dataSourceByName']['login']
            password = response['data']['dataSourceByName']['password']
            log.info('Connect to data source {data_source}.'.format(data_source=data_source))
            connection = utils.get_connection(data_source_type_id, connection_string, login, password)
        else:
            error_message = 'Data source {data_source} does not exist.'.format(data_source=data_source)
            log.error(error_message)
            raise Exception(error_message)

        # Get data frame
        log.info('Execute request on data source.'.format(data_source=data_source))
        data_frame = pandas.read_sql(request, connection)
        if data_frame.empty:
            log.debug('Request: {request}.'.format(request=request))
            error_message = 'Request on data source {data_source} returned no data.'.format(data_source=data_source)
            log.error(error_message)
            raise Exception(error_message)

        # Format data frame
        log.debug('Format data frame.')
        column_names = dimensions + measures
        data_frame.columns = column_names
        for column in dimensions:
            data_frame[column] = data_frame[column].astype(str)  # Convert dimension values to string

        return data_frame

    def is_alert(self, measure_value, alert_operator, alert_threshold):
        """
        Compare measure to alert threshold based on the alert operator.
        Return True if an alert must be sent, False otherwise.
        Supported alert operators are: ==, >, >=, <, <=, !=
        """
        if eval(str(measure_value) + alert_operator + str(alert_threshold)):
            return True
        else:
            return False

    def compute_session_result(self, session_id, alert_operator, alert_threshold, result_data):
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
        utils.execute_graphql_request(mutation)

        return nb_records_alert

    def send_alert(self, indicator_id, indicator_name, session_id, distribution_list, alert_operator, alert_threshold, nb_records_alert, result_data):
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
        utils.send_mail(distribution_list, 'indicator', file_path, **body)
        os.remove(file_path)

        return True
