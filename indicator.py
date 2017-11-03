#!/usr/bin/env python
"""Indicators related functions."""
from database import DbOperation
import argparse
import batch
import event
import importlib
import logging
import sys
import utils


# Load logger
utils.config_logger()
log = logging.getLogger(__name__)


def execute(indicator_id, batch_id):
    """Execute a data quality indicator."""
    event.log_event(indicator_id, batch_id, 'Session start')

    # Get indicator type
    with DbOperation('Indicator') as op:
        indicator_list = op.read(id=indicator_id)

    # Get indicator module and function
    with DbOperation('IndicatorType') as op:
        indicator_type_list = op.read(id=indicator_list[0].indicatorTypeId)

    # Import module and execute indicator function
    importlib.import_module(indicator_type_list[0].module)
    getattr(sys.modules[indicator_type_list[0].module], indicator_type_list[0].function)(indicator_id, batch_id)

    event.log_event(indicator_id, batch_id, 'Session stop')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Id', type=int, help='Enter the Id of the indicator you want to execute.')
    arguments = parser.parse_args()

    # Get batch owner of the indicator
    with DbOperation('Indicator') as op:
        indicator_list = op.read(id=arguments.Id)

    # Start batch
    batch_record = batch.log_batch(indicator_list[0].batchOwnerId, 'Batch start')

    # Execute indicator
    execute(arguments.Id, batch_record.id)

    # Stop batch
    batch.log_batch(indicator_list[0].batchOwnerId, 'Batch stop')
