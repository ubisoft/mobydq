#!/usr/bin/env python
"""Controls indicators execution and logs events."""
from api.database.operation import Operation
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

    If event is Start:
    * Insert a new batch
    * New batch status is set to Running (Id: 1)
    * Returns the corresponding batch object

    If event is Stop:
    * Terminate an existing running batch
    * Existing batch status is set to Succeeded (Id: 2)
    * Returns the corresponding batch object
    """
    # Verify batch owner exists
    batch_owner_list = Operation('BatchOwner').read(id=batch_owner_id)

    if not batch_owner_list:
        log.error('Cannot insert or update batch because batch owner Id {} does not exist'.format(batch_owner_id))
        return False

    # Verify event type exists
    event_type_list = Operation('EventType').read(name=event)

    if not event_type_list:
        log.error('Cannot insert or update batch because event type {} does not exist'.format(event))
        return False

    # Start new batch
    if event == 'Start':
        log.info('Starting batch for batch owner Id: {}'.format(batch_owner_id))
        # Verify there is no running batch
        batch_list = Operation('Batch').read(batchOwnerId=batch_owner_id, statusId=1)

        if batch_list:
            log.error('Cannot start batch because batch owner {} already has a running batch with batch Id: {}'.format(
                batch_owner_id, batch_list[0].id)
            )
            return False

        # Insert new running batch
        batch_list = Operation('Batch').create(batchOwnerId=batch_owner_id, statusId=1)

    # End running batch
    elif event == 'Stop':
        log.info('Stoping batch for batch owner Id: {}'.format(batch_owner_id))
        # Find current running batch
        batch_list = Operation('Batch').read(batchOwnerId=batch_owner_id, statusId=1)

        if not batch_list:
            log.error('Cannot end batch because batch owner Id {} does not have a running batch'.format(batch_owner_id))
            return False

        # Update running batch
        batch_list = Operation('Batch').update(id=batch_list[0].id, statusId=2)

    # Fail running batch
    elif event == 'Error':
        log.info('Failing batch for batch owner Id: {}'.format(batch_owner_id))
        # Find current running batch
        batch_list = Operation('Batch').read(batchOwnerId=batch_owner_id, statusId=1)

        if not batch_list:
            log.error('Cannot fail batch because batch owner Id {} does not have a running batch'.format(batch_owner_id))
            return False

        # Update running batch
        batch_list = Operation('Batch').update(id=batch_list[0].id, statusId=3)

    # Invalid event
    else:
        log.error('Invalid argument event: {}'.format(event))
        return False

    # Return record
    return batch_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Id', type=int, help='Enter the Id of the batch owner for which you want to run a batch.')
    arguments = parser.parse_args()

    # Start batch
    batch_record = log_batch(arguments.Id, 'Start')

    # Get indicators for the batch owner
    indicator_list = Operation('Indicator').read(batchOwnerId=arguments.Id)

    for indicator_record in indicator_list:
        indicator.execute(indicator_record.id, batch_record.id)

    # Stop batch
    log_batch(arguments.Id, 'Stop')
