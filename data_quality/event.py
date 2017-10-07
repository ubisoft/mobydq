"""Controls indicators execution and logs events."""
from database import DatabaseFunction
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
    with DatabaseFunction('BatchOwner') as function:
        batchownerlist = function.read(name=batchowner)

    if not batchownerlist:
        log.error('Cannot start batch because batch owner {} does not exist'.format(batchowner))
        return False

    # Start new batch
    if event == 'Batch start':
        # Verify there is no running batch
        with DatabaseFunction('Batch') as function:
            batchlist = function.read(batchOwnerId=batchownerlist[0].id, statusId=1)

        if batchlist:
            log.error('Cannot start batch because batch owner {} already has a running batch with batch Id: {}'.format(batchowner, batchlist[0].id))
            return False

        # Insert new running batch
        with DatabaseFunction('Batch') as function:
            batchlist = function.create(batchOwnerId=batchownerlist[0].id, statusId=1)

    # End running batch
    elif event == 'Batch stop':
        # Find current running batch
        with DatabaseFunction('Batch') as function:
            batchlist = function.read(batchOwnerId=batchownerlist[0].id, statusId=1)

        if not batchlist:
            log.error('Cannot end batch because batch owner {} does not have a running batch'.format(batchowner))
            return False

        # Update running batch
        with DatabaseFunction('Batch') as function:
            batchlist = function.update(id=batchlist[0].id, statusId=2)

    # Invalid event
    else:
        log.error('Invalid argument event: {}'.format(event))
        return False

    # Return first and only record in list
    return batchlist[0]


def logevent(indicatorid, batchid, event, dataset={}):
    """
    Manage session status and event logging for the corresponding data quality indicator. Return event object.

    If event is Session start:
    * Insert a new session
    * New session status is set to Running (Id: 1)
    * Insert a new Session start event
    * Returns the corresponding event object

    If event is Session stop:
    * Terminate an existing running session
    * Existing session status is set to Succeeded (Id: 2)
    * Insert a new Session stop event
    * Returns the corresponding event object

    If event is Error:
    * Terminate an existing running session
    * Existing session status is set to Failed (Id: 3)
    * Insert a new Error event
    * Returns the corresponding event object

    If event is Data set:
    * Existing session status remains unchanged
    * Insert a new Data set event
    * Returns the corresponding event object
    """
    # Verify indicator exists
    with DatabaseFunction('Indicator') as function:
        indicatorlist = function.read(id=indicatorid)

    if not indicatorlist:
        log.error('Cannot log event because indicator with Id {} does not exist'.format(indicatorid))
        return False

    # Verify batch exists and is running
    with DatabaseFunction('Batch') as function:
        batchlist = function.read(id=batchid, statusId=1)

    if not batchlist:
        log.error('Cannot log event because batch with Id {} does exist or is not running'.format(batchid))
        return False

    # Verify event type exists
    with DatabaseFunction('EventType') as function:
        eventtypelist = function.read(name=event)

    if not eventtypelist:
        log.error('Cannot log event because event type {} does exist'.format(event))
        return False

    # Log session start, insert new running session
    if event == 'Session start':
        # Verify current indicator is not running already
        with DatabaseFunction('Session') as function:
            sessionlist = function.read(indicatorId=indicatorid, batchId=batchid, statusId=1)

        if sessionlist:
            log.error('Cannot log {} event because indicator with Id {} already has a running session with batch Id {}'.format(event, indicatorid, batchid))
            return False

        # Insert new running session
        with DatabaseFunction('Session') as function:
            sessionlist = function.create(indicatorId=indicatorid, batchId=batchid, statusId=1)

        # Insert session start event
        with DatabaseFunction('Event') as function:
            eventlist = function.create(eventTypeId=eventtypelist[0].id, sessionId=sessionlist[0].id, content=dataset)

    # Log session stop, update running session to succeeded
    elif event == 'Session stop':
        # Verify current indicator is running
        with DatabaseFunction('Session') as function:
            sessionlist = function.read(indicatorId=indicatorid, batchId=batchid, statusId=1)

        if not sessionlist:
            log.error('Cannot log {} event because indicator with Id {} does not have a running session with batch Id {}'.format(event, indicatorid, batchid))
            return False

        # Insert session stop event
        with DatabaseFunction('Event') as function:
            eventlist = function.create(eventTypeId=eventtypelist[0].id, sessionId=sessionlist[0].id, content=dataset)

        # Update running session to succeeded
        with DatabaseFunction('Session') as function:
            sessionlist = function.update(id=sessionlist[0].id, statusId=2)

    # Log error, update running session to failed
    elif event == 'Error':
        # Verify current indicator is running
        with DatabaseFunction('Session') as function:
            sessionlist = function.read(indicatorId=indicatorid, batchId=batchid, statusId=1)

        if not sessionlist:
            log.error('Cannot log {} event because indicator with Id {} does not have a running session with batch Id {}'.format(event, indicatorid, batchid))
            return False

        # Insert error event
        with DatabaseFunction('Event') as function:
            eventlist = function.create(eventTypeId=eventtypelist[0].id, sessionId=sessionlist[0].id, content=dataset)

        # Update running session to failed
        with DatabaseFunction('Session') as function:
            sessionlist = function.update(id=sessionlist[0].id, statusId=3)

    # Log data set
    elif event == 'Data set':
        # Verify current indicator is running
        with DatabaseFunction('Session') as function:
            sessionlist = function.read(indicatorId=indicatorid, batchId=batchid, statusId=1)

        if not sessionlist:
            log.error('Cannot log {} event because indicator with Id {} does not have a running session with batch Id {}'.format(event, indicatorid, batchid))
            return False

        # Insert data set event
        with DatabaseFunction('Event') as function:
            eventlist = function.create(eventTypeId=eventtypelist[0].id, sessionId=sessionlist[0].id, content=dataset)

    # Invalid event
    else:
        log.error('Invalid argument event: {}'.format(event))
        return False

    return eventlist[0]
