"""Controls indicators execution and logs events."""
from database import Function
import logging
import utils

# Load logger
utils.configlogger()
log = logging.getLogger(__name__)


def logbatch(batchowner, event):
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
    with Function('BatchOwner') as function:
        batchownerlist = function.read(name=batchowner)

    if not batchownerlist:
        log.error('Cannot start batch because batch owner {} does not exist'.format(batchowner))
        return False

    # Start new batch
    if event == 'Batch start':
        # Verify there is no running batch
        with Function('Batch') as function:
            batchlist = function.read(batchOwnerId=batchownerlist[0].id, statusId=1)

        if batchlist:
            log.error('Cannot start batch because batch owner {} already has a running batch with batch Id: {}'.format(batchowner, batchlist[0].id))
            return False

        # Insert new running batch
        with Function('Batch') as function:
            batchlist = function.create(batchOwnerId=batchownerlist[0].id, statusId=1)

    # End running batch
    elif event == 'Batch stop':
        # Find current running batch
        with Function('Batch') as function:
            batchlist = function.read(batchOwnerId=batchownerlist[0].id, statusId=1)

        if not batchlist:
            log.error('Cannot end batch because batch owner {} does not have a running batch'.format(batchowner))
            return False

        # Update running batch
        with Function('Batch') as function:
            batchlist = function.update(id=batchlist[0].id, statusId=2)

    # Invalid event
    else:
        log.error('Invalid argument event: {}'.format(event))
        return False

    # Return first and only record in list
    return batchlist[0]
