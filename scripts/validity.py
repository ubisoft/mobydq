from indicator import Indicator
import logging
import pandas
import utils

# Load logging configuration
log = logging.getLogger(__name__)


class Validity(Indicator):
    """Class used to compute indicators of type validity."""

    def __init__(self):
        pass

    def execute(self, session):
        """Execute indicator of type validity."""
        # Update session status to running
        session_id = session['id']
        indicator_id = session['indicatorId']
        log.info('Start execution of session Id {session_id} for indicator Id {indicator_id}.'.format(session_id=session_id, indicator_id=indicator_id))
        log.debug('Update session status to Running.')
        utils.update_session_status(session_id, 'Running')

        # Verify if the list of indicator parameters is valid
        indicaor_type_id = session['indicatorByIndicatorId']['indicatorTypeId']
        parameters = session['indicatorByIndicatorId']['parametersByIndicatorId']['nodes']
        parameters = utils.verify_indicator_parameters(indicaor_type_id, parameters)

        # Get target data
        dimensions = parameters[4]
        measures = parameters[5]
        target = parameters[8]
        target_request = parameters[9]
        target_data = super().get_data_frame(target, target_request, dimensions, measures)

        # Evaluate completeness
        alert_operator = parameters[1]  # Alert operator
        alert_threshold = parameters[2]  # Alert threshold
        log.info('Evaluate validity of target data source.')
        result_data = self.evaluate_validity(target_data, measures, alert_operator, alert_threshold)

        # Compute session result
        log.info('Compute session results.')
        nb_records_alert = super().compute_session_result(session_id, alert_operator, alert_threshold, result_data)

        # Send e-mail alert
        if nb_records_alert != 0:
            indicator_name = session['indicatorByIndicatorId']['name']
            distribution_list = parameters[3]  # Distribution list
            super().send_alert(indicator_id, indicator_name, session_id, distribution_list, alert_operator, alert_threshold, nb_records_alert, result_data)

        # Update session status to succeeded
        log.debug('Update session status to Succeeded.')
        utils.update_session_status(session_id, 'Succeeded')
        log.info('Session Id {session_id} for indicator Id {indicator_id} completed successfully.'.format(session_id=session_id, indicator_id=indicator_id))

    def evaluate_validity(self, target_data, measures, alert_operator, alert_threshold):
        """Compute specificities of validity indicator and return results in a data frame."""
        # No tranformation needed for this data frame
        result_data = target_data

        # Formatting data to improve readability
        for measure in measures:
            result_data[measure] = round(result_data[measure], 2).astype(float)

        # For each record and measure in data frame test if alert must be sent and update alert column
        result_data['Alert'] = False
        for measure in measures:
            for row_num in result_data.index:
                measure_value = result_data.loc[row_num, measure]
                if self.is_alert(measure_value, alert_operator, alert_threshold):
                    result_data.loc[row_num, 'Alert'] = True

        return result_data
