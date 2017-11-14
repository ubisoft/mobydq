"""Utility functions used by API scripts."""
import logging

from database.operation import Operation as DbOperation

log = logging.getLogger(__name__)


def create(resource_name, payload=None):
    """Generic create function called by post methods in api.py."""
    if not payload:
        payload = {}

    record = DbOperation(resource_name).create(**payload)

    # Convert database object into json
    response = record.as_dict()
    return(response)


def read(resource_name, payload=None):
    """Generic read function called by get methods in api.py."""
    if not payload:
        payload = {}

    record_list = DbOperation(resource_name).read(**payload)

    # Convert database object into json
    response = []
    for record in record_list:
        response.append(record.as_dict())
    return(response)


def update(resource_name, payload=None):
    """Generic update function called by put methods in api.py."""
    if not payload:
        payload = {}

    record = DbOperation(resource_name).update(**payload)

    # Convert database object into json
    response = record.as_dict()
    return (response)


def delete(resource_name, payload=None):
    """Generic update function called by put methods in api.py."""
    if not payload:
        payload = {}

    DbOperation(resource_name).delete(**payload)
    return ({})


def _log_batch(batch_owner_id, event):
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
    batch_owner_list = DbOperation('BatchOwner').read(id=batch_owner_id)

    if not batch_owner_list:
        log.error('Cannot insert or update batch because batch owner Id {} does not exist'.format(batch_owner_id))
        return False

    # Verify event type exists
    event_type_list = DbOperation('EventType').read(name=event)

    if not event_type_list:
        log.error('Cannot insert or update batch because event type {} does not exist'.format(event))
        return False

    # Start new batch
    if event == 'Start':
        log.info('Starting batch for batch owner Id: {}'.format(batch_owner_id))
        # Verify there is no running batch
        batch_list = DbOperation('Batch').read(batchOwnerId=batch_owner_id, statusId=1)

        if batch_list:
            log.error('Cannot start batch because batch owner {} already has a running batch with batch Id: {}'.format(
                batch_owner_id, batch_list[0].id)
            )
            return False

        # Insert new running batch
        batch_list = DbOperation('Batch').create(batchOwnerId=batch_owner_id, statusId=1)

    # End running batch
    elif event == 'Stop':
        log.info('Stoping batch for batch owner Id: {}'.format(batch_owner_id))
        # Find current running batch
        batch_list = DbOperation('Batch').read(batchOwnerId=batch_owner_id, statusId=1)

        if not batch_list:
            log.error('Cannot end batch because batch owner Id {} does not have a running batch'.format(batch_owner_id))
            return False

        # Update running batch
        batch_list = DbOperation('Batch').update(id=batch_list[0].id, statusId=2)

    # Fail running batch
    elif event == 'Error':
        log.info('Failing batch for batch owner Id: {}'.format(batch_owner_id))
        # Find current running batch
        batch_list = DbOperation('Batch').read(batchOwnerId=batch_owner_id, statusId=1)

        if not batch_list:
            log.error('Cannot fail batch because batch owner Id {} does not have a running batch'.format(batch_owner_id))
            return False

        # Update running batch
        batch_list = DbOperation('Batch').update(id=batch_list[0].id, statusId=3)

    # Invalid event
    else:
        log.error('Invalid argument event: {}'.format(event))
        return False

    # Return record
    return batch_list


def log_batch(batch_owner_id, event):
    """Manage batch status for the corresponding batch owner."""
    batch_list = _log_batch(batch_owner_id, event)
    if batch_list:
        response = {'message': 'Batch status updated.'}
    else:
        response = {'message': 'Batch status was not updated due to invalid event.'}
    return (response)
