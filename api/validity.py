"""Validity functions."""
import indicator
import logging
import utils

# Load logging configuration
log = logging.getLogger(__name__)


def evaluate_validity(data_sets, parameters):
    """Compute specificities of validity indicator."""
    # No tranformation needed for this data frame
    result_data_frame = data_sets['Target data frame']

    # Prepare variables
    alert_operator = parameters['Alert operator']
    alert_threshold = parameters['Alert threshold']
    measure_list = parameters['Measures']

    # Formatting data to improve readability
    for measure in measure_list:
        result_data_frame[measure] = round(result_data_frame[measure], 2).astype(float)

    # For each record and measure in data frame, test if alert must be sent and update alert column
    result_data_frame['Alert'] = False
    for measure in measure_list:
        for row_num in result_data_frame.index:
            measure_value = result_data_frame.loc[row_num, measure]
            if indicator.is_alert(measure_value, alert_operator, alert_threshold):
                result_data_frame.loc[row_num, 'Alert'] = True
    return result_data_frame
