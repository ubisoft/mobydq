"""Manage class and methods for sessions."""
import logging
import pandas
import utils

# Load logging configuration
log = logging.getLogger(__name__)


class Session:
    """Session class."""

    def update_session_status(self, authorization: str, session_id: int, session_status: str):
        """Update a session status."""

        query = 'mutation updateSessionStatus($id: Int!, $sessionPatch: SessionPatch!){updateSessionById(input:{id: $id, sessionPatch: $sessionPatch}){session{status}}}'
        variables = {'id': session_id, 'sessionPatch': {'status': session_status}}
        payload = {'query': query, 'variables': variables}
        response = utils.execute_graphql_request(authorization, payload)

        return response

    def compute_session_result(self, authorization: str, session_id: int, alert_operator: str, alert_threshold: str, result_data: pandas.DataFrame):
        """Compute aggregated results for the indicator session."""

        log.info('Compute session results.')
        nb_records = len(result_data)
        nb_records_alert = len(result_data.loc[result_data['Alert'] == True]) # pylint: disable=C0121
        nb_records_no_alert = len(result_data.loc[result_data['Alert'] == False]) # pylint: disable=C0121

        # Post results to database
        query = 'mutation updateSessionResults($id: Int!, $sessionPatch: SessionPatch!){updateSessionById(input:{id: $id, sessionPatch: $sessionPatch}){session{id}}}'
        variables = {}
        variables['id'] = session_id
        variables['sessionPatch'] = {}
        variables['sessionPatch']['alertOperator'] = alert_operator
        variables['sessionPatch']['alertThreshold'] = float(alert_threshold)  # Alert threshold is stored as string in parameters and needs to be converted to float
        variables['sessionPatch']['nbRecordsNoAlert'] = nb_records_no_alert
        variables['sessionPatch']['nbRecordsAlert'] = nb_records_alert
        variables['sessionPatch']['nbRecords'] = nb_records
        payload = {'query': query, 'variables': variables}
        utils.execute_graphql_request(authorization, payload)

        return nb_records_alert
