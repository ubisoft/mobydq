"""Manage class and methods for data validity indicators."""
import logging
import pandas
from indicator import Indicator
from session import Session

# Load logging configuration
log = logging.getLogger(__name__)


class Validity(Indicator):
    """Class used to compute indicators of type validity."""

    def execute(self, authorization: str, session: dict):
        """Execute indicator of type validity."""

        # Update session status to running
        session_id = session['id']
        indicator_id = session['indicatorId']
        log.info('Start execution of session Id %i for indicator Id %i.', session_id, indicator_id)
        log.debug('Update session status to Running.')
        Session().update_session_status(authorization, session_id, 'Running')

        # Verify if the list of indicator parameters is valid
        indicator_type_id = session['indicatorByIndicatorId']['indicatorTypeId']
        parameters = session['indicatorByIndicatorId']['parametersByIndicatorId']['nodes']
        parameters = super().verify_indicator_parameters(authorization, indicator_type_id, parameters)

        # Get target data
        dimensions = parameters[4]
        measures = parameters[5]
        target = parameters[8]
        target_request = parameters[9]
        target_data = super().get_data_frame(authorization, target, target_request, dimensions, measures)

        # Evaluate completeness
        alert_operator = parameters[1]  # Alert operator
        alert_threshold = parameters[2]  # Alert threshold
        log.info('Evaluate validity of target data source.')
        result_data = self.evaluate_validity(target_data, measures, alert_operator, alert_threshold)

        # Compute session result
        nb_records_alert = Session().compute_session_result(authorization, session_id, alert_operator, alert_threshold, result_data)

        # Send e-mail alert
        if nb_records_alert != 0:
            indicator_name = session['indicatorByIndicatorId']['name']
            distribution_list = parameters[3]  # Distribution list
            super().send_alert(indicator_id, indicator_name, session_id, distribution_list, alert_operator, alert_threshold, nb_records_alert, result_data)

        # Update session status to succeeded
        log.debug('Update session status to Success.')
        Session().update_session_status(authorization, session_id, 'Success')
        log.info('Session Id %i for indicator Id %i completed successfully.', session_id, indicator_id)

    def evaluate_validity(self, target_data: pandas.DataFrame, measures: str, alert_operator: str, alert_threshold: str):
        """Compute specificities of validity indicator and return results in a data frame."""

        # No tranformation needed for this data frame
        result_data = target_data
        result_data = result_data.fillna(value=0)  # Replace NaN values per 0

        # Formatting data to improve readability
        for measure in measures:
            result_data[measure] = round(result_data[measure], 2).astype(float)

        # For each record and measure in data frame test if alert must be sent and update alert column
        result_data['Alert'] = False
        for measure in measures:
            for row_num in result_data.index:
                measure_value = result_data.loc[row_num, measure]
                if self.is_alert(str(measure_value), alert_operator, alert_threshold):
                    result_data.loc[row_num, 'Alert'] = True

        return result_data
