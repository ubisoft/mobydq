"""Controls indicators execution and logs events."""
from database import Function
import logging
import utils

# Load logger
utils.configlogger()
log = logging.getLogger(__name__)


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
    with Function('Indicator') as function:
        indicatorlist = function.read(id=indicatorid)

    if not indicatorlist:
        log.error('Cannot log event because indicator with Id {} does not exist'.format(indicatorid))
        return False

    # Verify batch exists and is running
    with Function('Batch') as function:
        batchlist = function.read(id=batchid, statusId=1)

    if not batchlist:
        log.error('Cannot log event because batch with Id {} does exist or is not running'.format(batchid))
        return False

    # Verify event type exists
    with Function('EventType') as function:
        eventtypelist = function.read(name=event)

    if not eventtypelist:
        log.error('Cannot log event because event type {} does exist'.format(event))
        return False

    # Log session start, insert new running session
    if event == 'Session start':
        # Verify current indicator is not running already
        with Function('Session') as function:
            sessionlist = function.read(indicatorId=indicatorid, batchId=batchid, statusId=1)

        if sessionlist:
            log.error('Cannot log {} event because indicator with Id {} already has a running session with batch Id {}'.format(event, indicatorid, batchid))
            return False

        # Insert new running session
        with Function('Session') as function:
            session = function.create(indicatorId=indicatorid, batchId=batchid, statusId=1)

        # Insert session start event
        with Function('Event') as function:
            event = function.create(eventTypeId=eventtypelist[0].id, sessionId=session.id, content=dataset)

    # Log session stop, update running session to succeeded
    elif event == 'Session stop':
        # Verify current indicator is running
        with Function('Session') as function:
            sessionlist = function.read(indicatorId=indicatorid, batchId=batchid, statusId=1)

        if not sessionlist:
            log.error('Cannot log {} event because indicator with Id {} does not have a running session with batch Id {}'.format(event, indicatorid, batchid))
            return False

        # Insert session stop event
        with Function('Event') as function:
            event = function.create(eventTypeId=eventtypelist[0].id, sessionId=sessionlist[0].id, content=dataset)

        # Update running session to succeeded
        with Function('Session') as function:
            function.update(id=sessionlist[0].id, statusId=2)

    # Log error, update running session to failed
    elif event == 'Error':
        # Verify current indicator is running
        with Function('Session') as function:
            sessionlist = function.read(indicatorId=indicatorid, batchId=batchid, statusId=1)

        if not sessionlist:
            log.error('Cannot log {} event because indicator with Id {} does not have a running session with batch Id {}'.format(event, indicatorid, batchid))
            return False

        # Insert error event
        with Function('Event') as function:
            event = function.create(eventTypeId=eventtypelist[0].id, sessionId=sessionlist[0].id, content=dataset)

        # Update running session to failed
        with Function('Session') as function:
            function.update(id=sessionlist[0].id, statusId=3)

    # Log data set
    elif event == 'Data set':
        # Verify current indicator is running
        with Function('Session') as function:
            sessionlist = function.read(indicatorId=indicatorid, batchId=batchid, statusId=1)

        if not sessionlist:
            log.error('Cannot log {} event because indicator with Id {} does not have a running session with batch Id {}'.format(event, indicatorid, batchid))
            return False

        # Insert data set event
        with Function('Event') as function:
            event = function.create(eventTypeId=eventtypelist[0].id, sessionId=sessionlist[0].id, content=dataset)

    # Invalid event
    else:
        log.error('Invalid argument event: {}'.format(event))
        return False

    return event
