"""Completeness functions."""
import indicator
import logging
import pandas
import utils

# Load logging configuration
log = logging.getLogger(__name__)


def evaluate_completeness(data_sets, parameters):
    """Compute specificities of completeness indicator."""
    source_data_frame = data_sets['Source data frame']
    target_data_frame = data_sets['Target data frame']

    # Merge data frames to compare their measures
    result_data_frame = pandas.merge(
        left=source_data_frame,
        right=target_data_frame,
        left_on=parameters['Dimensions'],
        right_on=parameters['Dimensions'],
        how='outer',
        sort=True,
        suffixes=('_source', '_target'))
    result_data_frame = result_data_frame.fillna(value=0)  # Replace NaN values per 0

    # Prepare variables
    alert_operator = parameters['Alert operator']
    alert_threshold = parameters['Alert threshold']
    measure_list = parameters['Measures']

    # Compute delta and delta percentage between source and target measures
    for measure in measure_list:
        source_column = measure + '_source'
        target_column = measure + '_target'
        delta_column = measure + '_delta'
        delta_percentage_column = measure + '_delta_percentage'

        # Compute delta
        delta = result_data_frame[target_column] - result_data_frame[source_column]
        result_data_frame[delta_column] = delta

        # Compute delta percentage
        result_data_frame[delta_percentage_column] = result_data_frame[delta_column] / result_data_frame[source_column]
        result_data_frame.loc[(result_data_frame[source_column] == 0), delta_percentage_column] = 1  # Replace delta percentage by 1 since you can't divide by 0
        result_data_frame.loc[(result_data_frame[delta_column] == 0), delta_percentage_column] = 0  # Replace delta percentage by 0 since delta equal 0

        # Formatting data to improve readability
        result_data_frame[source_column] = round(result_data_frame[source_column], 2).astype(float)
        result_data_frame[target_column] = round(result_data_frame[target_column], 2).astype(float)
        result_data_frame[delta_column] = round(result_data_frame[delta_column], 2).astype(float)
        result_data_frame[delta_percentage_column] = round(result_data_frame[delta_percentage_column], 6).astype(float)

    # For each record and measure in data frame, test if alert must be sent and update alert column
    result_data_frame['Alert'] = False
    for measure in measure_list:
        for row_num in result_data_frame.index:
            measure_value = result_data_frame.loc[row_num, measure + '_delta_percentage']
            measure_value = abs(measure_value)*100
            if indicator.is_alert(measure_value, alert_operator, alert_threshold):
                result_data_frame.loc[row_num, 'Alert'] = True
    return result_data_frame
