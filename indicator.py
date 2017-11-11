#!/usr/bin/env python
"""Indicators related functions."""
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

    # Get indicator type
    with DbOperation('Indicator') as op:
        indicator_list = op.read(id=indicator_id)

    # Get indicator module and function
    with DbOperation('IndicatorType') as op:
        indicator_type_list = op.read(id=indicator_list[0].indicatorTypeId)

    # Import module and execute indicator function
    importlib.import_module(indicator_type_list[0].module)
    getattr(sys.modules[indicator_type_list[0].module], indicator_type_list[0].function)(indicator_id, event_session_start.sessionId)

    event.log_event(indicator_id, batch_id, 'Stop')


def get_data_set(data_source_name, request):
    """Connect to a data source, execute request and return the corresponding results as a pandas dataframe."""
    # Identify the type of data source
    with DbOperation('DataSource') as op:
        data_source_list = op.read(name=data_source_name)

    if not data_source_list:
        log.error('No {} found with values: {}'.format('DataSource', {'name': data_source_name}))
    else:
        data_source = data_source_list[0]

    # Database
    if data_source.dataSourceTypeId == 1:
        connection = utils.get_odbc_connection(data_source)
        data_set = pandas.read_sql(request, connection)

    # Api
    elif data_source.dataSourceTypeId == 2:
        # Not implemented yet
        pass

    # File
    elif data_source.dataSourceTypeId == 3:
        # Not implemented yet
        pass

    else:
        log.error('Unknown data source type Id: {}'.format(data_source_list[0].dataSourceTypeId))

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


def compute_indicator_result(data_set, indicator_id, session_id, alert_operator, alert_threshold):
    # Compute aggregates
    log.info('Computing aggregates for indicator Id {} and session Id {}'.format(indicator_id, session_id))
    nb_records = len(data_set)
    nb_records_alert = len(data_set.loc[data_set['Alert'] == True])
    nb_records_no_alert = len(data_set.loc[data_set['Alert'] == False])

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
