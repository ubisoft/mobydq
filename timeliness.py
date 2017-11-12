"""Timeliness functions."""
from datetime import datetime
import indicator
import logging
import pandas
import utils

# Load logger
utils.config_logger()
log = logging.getLogger(__name__)


def evaluate_freshness(data_sets, parameters):
    """Compute specificities of freshness indicator."""
    result_data_frame = data_sets['Target data frame']
    result_data_frame['current_timestamp'] = datetime.utcnow()

    # Prepare variables
    alert_operator = parameters['Alert operator']
    alert_threshold = parameters['Alert threshold']
    measure_list = parameters['Measures']

    # Compute delta in minutes and delta description between source and target measures
    for measure in measure_list:
        source_column = 'current_timestamp'
        target_column = measure
        delta_column = measure + '_delta_minutes'
        delta_description_column = measure + '_delta_description'

        # Enforce measure to datetime data type
        result_data_frame[source_column] = pandas.to_datetime(result_data_frame[source_column], format='%Y-%m-%d %H:%M:%S.%f', errors='ignore')
        result_data_frame[target_column] = pandas.to_datetime(result_data_frame[target_column], format='%Y-%m-%d %H:%M:%S.%f', errors='ignore')

        # Compute delta and delta description
        delta_seconds = (result_data_frame[source_column] - result_data_frame[target_column]).dt.total_seconds()
        result_data_frame[delta_column] = round(delta_seconds/60).astype(int)
        result_data_frame[delta_description_column] = pandas.to_timedelta(delta_seconds, unit='s')

    # For each record and measure in data frame, test if alert must be sent and update alert column
    result_data_frame['Alert'] = False
    for measure in measure_list:
        for row_num in result_data_frame.index:
            measure_value = result_data_frame.loc[row_num, measure + '_delta_minutes']
            measure_value = abs(measure_value)*100
            if indicator.is_alert(measure_value, alert_operator, alert_threshold):
                result_data_frame.loc[row_num, 'Alert'] = True
    return result_data_frame


def evaluate_latency(data_sets, parameters):
    """Compute specificities of latency indicator."""
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

    # Prepare variables
    alert_operator = parameters['Alert operator']
    alert_threshold = parameters['Alert threshold']
    measure_list = parameters['Measures']

    # Compute delta in minutes and delta description between source and target measures
    for measure in measure_list:
        source_column = measure + '_source'
        target_column = measure + '_target'
        delta_column = measure + '_delta_minutes'
        delta_description_column = measure + '_delta_description'

        # Enforce measure to datetime data type
        result_data_frame[source_column] = pandas.to_datetime(result_data_frame[source_column], format='%Y-%m-%d %H:%M:%S.%f', errors='ignore')
        result_data_frame[target_column] = pandas.to_datetime(result_data_frame[target_column], format='%Y-%m-%d %H:%M:%S.%f', errors='ignore')

        # Compute delta and delta description
        delta_seconds = (result_data_frame[source_column] - result_data_frame[target_column]).dt.total_seconds()
        result_data_frame[delta_column] = round(delta_seconds/60).astype(int)
        result_data_frame[delta_description_column] = pandas.to_timedelta(delta_seconds, unit='s')

    # For each record and measure in data frame, test if alert must be sent and update alert column
    result_data_frame['Alert'] = False
    for measure in measure_list:
        for row_num in result_data_frame.index:
            measure_value = result_data_frame.loc[row_num, measure + '_delta_minutes']
            measure_value = abs(measure_value)*100
            if indicator.is_alert(measure_value, alert_operator, alert_threshold):
                result_data_frame.loc[row_num, 'Alert'] = True
    return result_data_frame
