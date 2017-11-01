#!/usr/bin/env python
"""Controls indicators execution and logs events."""
from database import DbOperation
import argparse
import indicator
import logging
import utils

# Load logger
utils.config_logger()
log = logging.getLogger(__name__)


def log_batch(batch_owner_id, event):
    """
    Manage batch status for the corresponding batch owner. Return batch object.

    If event is Batch start:
    * Insert a new batch
    * New batch status is set to Running (Id: 1)
    * Returns the corresponding batch object

    If event is Batch stop:
    * Terminate an existing running batch
    * Existing batch status is set to Succeeded (Id: 2)
    * Returns the corresponding batch object
    """
    # Verify batch owner exists
    with DbOperation('BatchOwner') as op:
        batchownerlist = op.read(id=batch_owner_id)

    if not batchownerlist:
        log.error('Cannot start batch because batch owner Id {} does not exist'.format(batch_owner_id))
        return False

    # Start new batch
    if event == 'Batch start':
        # Verify there is no running batch
        with DbOperation('Batch') as op:
            batchlist = op.read(batchOwnerId=batch_owner_id, statusId=1)

        if batchlist:
            log.error('Cannot start batch because batch owner {} already has a running batch with batch Id: {}'.format(batch_owner_id, batchlist[0].id))
            return False

        # Insert new running batch
        with DbOperation('Batch') as op:
            batchlist = op.create(batchOwnerId=batch_owner_id, statusId=1)

    # End running batch
    elif event == 'Batch stop':
        # Find current running batch
        with DbOperation('Batch') as op:
            batchlist = op.read(batchOwnerId=batch_owner_id, statusId=1)

        if not batchlist:
            log.error('Cannot end batch because batch owner Id {} does not have a running batch'.format(batch_owner_id))
            return False

        # Update running batch
        with DbOperation('Batch') as op:
            batchlist = op.update(id=batchlist[0].id, statusId=2)

    # Invalid event
    else:
        log.error('Invalid argument event: {}'.format(event))
        return False

    # Return record
    return batchlist


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Id', type=int, help='Enter the Id of the batch owner for which you want to run a batch.')
    arguments = parser.parse_args()

    # Start batch
    batch_record = log_batch(arguments.Id, 'Batch start')

    # Get indicators for the batch owner
    with DbOperation('Indicator') as op:
        indicatorlist = op.read(batchOwnerId=arguments.Id)

    for indicatorrecord in indicatorlist:
        indicator.execute(indicatorrecord.id, batch_record.id)

    # Stop batch
    log_batch(arguments.Id, 'Batch stop')
