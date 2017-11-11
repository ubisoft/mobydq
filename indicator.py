#!/usr/bin/env python
"""Indicators related functions."""
from ast import literal_eval
from database import DbOperation
import argparse
import batch
import event
import importlib
import logging
import pandas
import sys
import traceback
import utils


# Load logger
utils.config_logger()
log = logging.getLogger(__name__)


def execute(indicator_id, batch_id):
    """Execute a data quality indicator."""
    event_session_start = event.log_event(indicator_id, batch_id, 'Start')
    session_id = event_session_start.sessionId

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

    # Get source and target data sets
    data_sets = {}
    for parameter in parameters:
        if parameter == 'Source':
            log.info('Getting data set from {} data source: {}'.format(parameter, parameters[parameter]))
            data_sets['Source data frame'] = get_data_set(parameters[parameter], parameters['Source request'])

        elif parameter == 'Target':
            log.info('Getting data set from {} data source: {}'.format(parameter, parameters[parameter]))
            data_sets['Target data frame'] = get_data_set(parameters[parameter], parameters['Target request'])

    # Format source and target data set with dimensions and measures parameters
    for data_set in data_sets:
        log.info('Formatting {}'.format(data_set))
        data_frame = data_sets[data_set]
        column_name_list = parameters['Dimensions'] + parameters['Measures']
        data_frame.columns = column_name_list
        for column in parameters['Dimensions']:
            data_frame[column] = data_frame[column].astype(str)
        data_sets[data_set] = data_frame

    # Get indicator type
    with DbOperation('Indicator') as op:
        indicator_list = op.read(id=indicator_id)

    # Get indicator module and function
    with DbOperation('IndicatorType') as op:
        indicator_type_list = op.read(id=indicator_list[0].indicatorTypeId)

    # Import module and execute specific indicator function
    importlib.import_module(indicator_type_list[0].module)
    result_data_frame = getattr(sys.modules[indicator_type_list[0].module], indicator_type_list[0].function)(data_sets, parameters)

    # Compute aggregated indicator results
    log.info('Computing aggregated results for indicator Id: {}'.format(indicator_id))
    compute_indicator_result(indicator_id, session_id, parameters, result_data_frame)

    # Send e-mail alert
    if not result_data_frame.loc[result_data_frame['Alert'] == True].empty:
        log.info('Sending e-mail alert for indicator Id {} and session Id {}'.format(indicator_id, session_id))
        # Send e-mail function to be implemented

    event.log_event(indicator_id, batch_id, 'Stop')


def get_data_set(data_source_name, request):
    """Connect to a data source, execute request and return the corresponding results as a pandas dataframe."""
    # Get data source
    with DbOperation('DataSource') as op:
        data_source_list = op.read(name=data_source_name)

    if not data_source_list:
        log.error('No {} found with values: {}'.format('DataSource', {'name': data_source_name}))
    else:
        data_source = data_source_list[0]

    # Identify the type of data source
    with DbOperation('DataSourceType') as op:
        data_source_type_list = op.read(id=data_source.dataSourceTypeId)

    if not data_source_type_list:
        log.error('No {} found with values: {}'.format('DataSourceType', {'id': data_source.dataSourceTypeId}))
    else:
        data_source_type = data_source_type_list[0]

    # Database
    if data_source_type.type == 'Database':
        connection = utils.get_database_connection(data_source)
        data_set = pandas.read_sql(request, connection)

    # File
    elif data_source_type.type == 'File':
        # Not implemented yet
        pass

    # API
    elif data_source_type.type == 'API':
        # Not implemented yet
        pass

    else:
        log.error('Unknown data source type: {}'.format(data_source_type.type))

    return data_set


def is_alert(measure_value, alert_operator, alert_threshold):
    """
    Compare measure to alert threshold based on the alert operator, return True if an alert must be sent, False otherwise.

    Supported alert operators are: ==, >, >=, <, <=, !=
    """
    if eval(str(measure_value) + alert_operator + str(alert_threshold)):
        return True
    else:
        return False


def compute_indicator_result(indicator_id, session_id, parameters, result_data_frame):
    # Compute aggregates
    alert_operator = parameters['Alert operator']
    alert_threshold = parameters['Alert threshold']
    nb_records = len(result_data_frame)
    nb_records_alert = len(result_data_frame.loc[result_data_frame['Alert'] == True])
    nb_records_no_alert = len(result_data_frame.loc[result_data_frame['Alert'] == False])

    # Insert result to database
    with DbOperation('IndicatorResult') as op:
        op.create(
            indicatorId=indicator_id,
            sessionId=session_id,
            alertOperator=alert_operator,
            alertThreshold=alert_threshold,
            nbRecords=nb_records,
            nbRecordsAlert=nb_records_alert,
            nbRecordsNoAlert=nb_records_no_alert)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Id', type=int, help='Enter the Id of the indicator you want to execute.')
    arguments = parser.parse_args()

    # Get batch owner of the indicator
    with DbOperation('Indicator') as op:
        indicator_list = op.read(id=arguments.Id)

    # Start batch
    batch_record = batch.log_batch(indicator_list[0].batchOwnerId, 'Start')

    try:
        # Execute indicator
        execute(arguments.Id, batch_record.id)

        # Stop batch
        batch.log_batch(indicator_list[0].batchOwnerId, 'Stop')
    except Exception as e:
        # Fail batch
        batch.log_batch(indicator_list[0].batchOwnerId, 'Error')
        log.error('Error encountered when computing indicator Id: {}'.format(arguments.Id))
        log.error('Traceback: \n {}'.format(traceback.format_exc()))
