from indicator import Indicator
import logging
import pandas
import utils

# Load logging configuration
log = logging.getLogger(__name__)


class Completeness(Indicator):
    """Class used to compute indicators of type completeness."""

    def __init__(self):
        pass

    def execute(self, session):
        """Execute indicator of type completeness."""
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

        # Get source data
        dimensions = parameters[4]
        measures = parameters[5]
        source = parameters[6]
        source_request = parameters[7]
        source_data = super().get_data_frame(source, source_request, dimensions, measures)

        # Get target data
        target = parameters[8]
        target_request = parameters[9]
        target_data = super().get_data_frame(target, target_request, dimensions, measures)

        # Evaluate completeness
        alert_operator = parameters[1]  # Alert operator
        alert_threshold = parameters[2]  # Alert threshold
        log.info('Evaluate completeness of target data source.')
        result_data = self.evaluate_completeness(source_data, target_data, dimensions, measures, alert_operator, alert_threshold)

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

    def evaluate_completeness(self, source_data, target_data, dimensions, measures, alert_operator, alert_threshold):
        """Compute specificities of completeness indicator and return results in a data frame."""
        # Merge data frames to compare their measures
        result_data = pandas.merge(
            left=source_data,
            right=target_data,
            left_on=dimensions,
            right_on=dimensions,
            how='outer',
            sort=True,
            suffixes=('_source', '_target'))
        result_data = result_data.fillna(value=0)  # Replace NaN values per 0

        # Compute delta and delta percentage between source and target measures
        for measure in measures:
            source_column = measure + '_source'
            target_column = measure + '_target'
            delta_column = measure + '_delta'
            delta_percentage_column = measure + '_delta_percentage'

            # Compute delta
            delta = result_data[target_column] - result_data[source_column]
            result_data[delta_column] = delta

            # Compute delta percentage
            result_data[delta_percentage_column] = result_data[delta_column] / result_data[source_column]
            result_data.loc[(result_data[source_column] == 0), delta_percentage_column] = 1  # Replace delta percentage by 1 since can't divide by 0
            result_data.loc[(result_data[delta_column] == 0), delta_percentage_column] = 0  # Replace delta percentage by 0 since delta equal 0

            # Formatting data to improve readability
            result_data[source_column] = round(result_data[source_column], 2).astype(float)
            result_data[target_column] = round(result_data[target_column], 2).astype(float)
            result_data[delta_column] = round(result_data[delta_column], 2).astype(float)
            result_data[delta_percentage_column] = round(result_data[delta_percentage_column], 6).astype(float)

        # For each record and measure in data frame test if alert must be sent and update alert column
        result_data['Alert'] = False
        for measure in measures:
            for row_num in result_data.index:
                measure_value = result_data.loc[row_num, measure + '_delta_percentage']
                measure_value = abs(measure_value)*100  # Multiply by 100 to format to percentage
                if super().is_alert(measure_value, alert_operator, alert_threshold):
                    result_data.loc[row_num, 'Alert'] = True

        return result_data
