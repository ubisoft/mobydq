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

        mutation = 'mutation{updateSessionById(input:{id:session_id,sessionPatch:{status:"session_status"}}){session{status}}}'
        mutation = mutation.replace('session_id', str(session_id))  # Use replace() instead of format() because of curly braces
        mutation = mutation.replace('session_status', str(session_status))  # Use replace() instead of format() because of curly braces
        mutation = {'query': mutation}  # Convert to dictionary
        data = utils.execute_graphql_request(authorization, mutation)

        return data

    def compute_session_result(self, authorization: str, session_id: int, alert_operator: str, alert_threshold: str, result_data: pandas.DataFrame):
        """Compute aggregated results for the indicator session."""

        log.info('Compute session results.')
        nb_records = len(result_data)
        nb_records_alert = len(result_data.loc[result_data['Alert'] == True]) # pylint: disable=C0121
        nb_records_no_alert = len(result_data.loc[result_data['Alert'] == False]) # pylint: disable=C0121

        # Post results to database
        mutation = '''mutation{updateSessionById(input:{id:session_id,sessionPatch:{alertOperator:"alert_operator",alertThreshold:alert_threshold,nbRecords:nb_records,nbRecordsAlert:nb_records_alert,nbRecordsNoAlert:nb_records_no_alert}}){session{id}}}'''

        # Use replace() instead of format() because of curly braces
        mutation = mutation.replace('session_id', str(session_id))
        mutation = mutation.replace('alert_operator', alert_operator)
        mutation = mutation.replace('alert_threshold', str(alert_threshold))
        mutation = mutation.replace('nb_records_no_alert', str(nb_records_no_alert))  # Order matters to avoid replacing other strings nb_records
        mutation = mutation.replace('nb_records_alert', str(nb_records_alert))  # Order matters to avoid replacing other strings nb_records
        mutation = mutation.replace('nb_records', str(nb_records))  # Order matters to avoid replacing other strings nb_records
        mutation = {'query': mutation}  # Convert to dictionary
        utils.execute_graphql_request(authorization, mutation)

        return nb_records_alert
