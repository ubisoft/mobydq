"""Validity functions."""
from ast import literal_eval
from database import DbOperation
import indicator
import logging
import pandas
import utils

# Load logger
utils.config_logger()
log = logging.getLogger(__name__)


def evaluate_validity(indicator_id, session_id):
    """Compute validity indicator."""
    # Get indicator parameters
    with DbOperation('IndicatorParameter') as op:
        indicator_parameter_list = op.read(indicatorId=indicator_id)

    # Create dictionary from indicator parameters
    parameters = {}
    for indicator_parameter in indicator_parameter_list:
        parameters[indicator_parameter.name] = indicator_parameter.value

    # Convert list parameters to list objects
    parameters['Dimensions'] = literal_eval(parameters['Dimensions'])
    parameters['Measures'] = literal_eval(parameters['Measures'])
    parameters['Distribution list'] = literal_eval(parameters['Distribution list'])

    # Get target data set
    log.info('Getting data set from target data source: {}'.format(parameters['Target']))
    data_set = indicator.get_data_set(parameters['Target'], parameters['Target request'])

    # Format data set with dimensions and measures parameters
    log.info('Formatting data set from target data source: {}'.format(parameters['Target']))
    column_name_list = parameters['Dimensions'] + parameters['Measures']
    data_set.columns = column_name_list
    for column in parameters['Dimensions']:
        data_set[column] = data_set[column].astype(str)

    # For each record and measure in data set, test if alert must be sent
    data_set['Alert'] = False
    alert_operator = parameters['Alert operator']
    alert_threshold = parameters['Alert threshold']
    for measure in parameters['Measures']:
        for row_num in data_set.index:
            measure_value = data_set.loc[row_num, measure]
            data_set.loc[row_num, 'Alert'] = indicator.is_alert(measure_value, alert_operator, alert_threshold)
    print(data_set)
    # Compute aggregated indicator results
    log.info('Computing indicator results for indicator Id: {}'.format(indicator_id))
    indicator.compute_indicator_result(data_set, indicator_id, session_id, alert_operator, alert_threshold)

    # Send e-mail alert
    if not data_set.loc[data_set['Alert'] == True].empty:
        log.info('Sending e-mail alert for indicator Id {} and session Id {}'.format(indicator_id, session_id))
        # Send e-mail function to be implemented

    return True
