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


def execute(indicatorid, batchid):
    """Execute a data quality indicator."""
    event.logevent(indicatorid, batchid, 'Session start')

    # Get indicator type
    with DbOperation('Indicator') as op:
        indicatorlist = op.read(id=indicatorid)

    # Get indicator module and function
    with DbOperation('IndicatorType') as op:
        indicatortypelist = op.read(id=indicatorlist[0].indicatorTypeId)

    # Import module and execute indicator function
    importlib.import_module(indicatortypelist[0].module)
    getattr(sys.modules[indicatortypelist[0].module], indicatortypelist[0].function)(indicatorid, batchid)

    event.logevent(indicatorid, batchid, 'Session stop')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Id', type=int, help='Enter the Id of the indicator you want to execute.')
    arguments = parser.parse_args()

    # Get batch owner of the indicator
    with DbOperation('Indicator') as op:
        indicatorlist = op.read(id=arguments.Id)

    # Start batch
    batchrecord = batch.logbatch(indicatorlist[0].batchOwnerId, 'Batch start')

    # Execute indicator
    execute(arguments.Id, batchrecord.id)

    # Stop batch
    batch.logbatch(indicatorlist[0].batchOwnerId, 'Batch stop')
