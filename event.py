"""Controls indicators execution and logs events."""
from database import DbOperation
import logging
import utils

# Load logger
utils.config_logger()
log = logging.getLogger(__name__)


def log_event(indicator_id, batch_id, event, data_set=None):
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
    if not data_set:
        data_set = {}
    # Verify indicator exists
    with DbOperation('Indicator') as op:
        indicator_list = op.read(id=indicator_id)

    if not indicator_list:
        log.error('Cannot log event because indicator with Id {} does not exist'.format(indicator_id))
        return False

    # Verify batch exists and is running
    with DbOperation('Batch') as op:
        batch_list = op.read(id=batch_id, statusId=1)

    if not batch_list:
        log.error('Cannot log event because batch with Id {} does exist or is not running'.format(batch_id))
        return False

    # Verify event type exists
    with DbOperation('EventType') as op:
        event_type_list = op.read(name=event)

    if not event_type_list:
        log.error('Cannot log event because event type {} does exist'.format(event))
        return False

    # Log session start, insert new running session
    if event == 'Session start':
        log.info('Starting session for indicator Id: {}'.format(indicator_id))

        # Verify current indicator is not running already
        with DbOperation('Session') as op:
            session_list = op.read(indicatorId=indicator_id, batchId=batch_id, statusId=1)

        if session_list:
            log.error('Cannot log {} event because indicator with Id {} already has a running session with batch Id {}'.format(event, indicator_id, batch_id))
            return False

        # Insert new running session
        with DbOperation('Session') as op:
            session = op.create(indicatorId=indicator_id, batchId=batch_id, statusId=1)

        # Insert session start event
        with DbOperation('Event') as op:
            event = op.create(eventTypeId=event_type_list[0].id, sessionId=session.id, content=data_set)

    # Log session stop, update running session to succeeded
    elif event == 'Session stop':
        log.info('Stoping session for indicator Id: {}'.format(indicator_id))

        # Verify current indicator is running
        with DbOperation('Session') as op:
            session_list = op.read(indicatorId=indicator_id, batchId=batch_id, statusId=1)

        if not session_list:
            log.error('Cannot log {} event because indicator with Id {} does not have a running session with batch Id {}'.format(event, indicator_id, batch_id))
            return False

        # Insert session stop event
        with DbOperation('Event') as op:
            event = op.create(eventTypeId=event_type_list[0].id, sessionId=session_list[0].id, content=data_set)

        # Update running session to succeeded
        with DbOperation('Session') as op:
            op.update(id=session_list[0].id, statusId=2)

    # Log error, update running session to failed
    elif event == 'Error':
        log.info('Failing session for indicator Id: {}'.format(indicator_id))

        # Verify current indicator is running
        with DbOperation('Session') as op:
            session_list = op.read(indicatorId=indicator_id, batchId=batch_id, statusId=1)

        if not session_list:
            log.error('Cannot log {} event because indicator with Id {} does not have a running session with batch Id {}'.format(event, indicator_id, batch_id))
            return False

        # Insert error event
        with DbOperation('Event') as op:
            event = op.create(eventTypeId=event_type_list[0].id, sessionId=session_list[0].id, content=data_set)

        # Update running session to failed
        with DbOperation('Session') as op:
            op.update(id=session_list[0].id, statusId=3)

    # Log data set
    elif event == 'Data set':
        log.info('Logging data set for indicator Id: {}'.format(indicator_id))

        # Verify current indicator is running
        with DbOperation('Session') as op:
            session_list = op.read(indicatorId=indicator_id, batchId=batch_id, statusId=1)

        if not session_list:
            log.error('Cannot log {} event because indicator with Id {} does not have a running session with batch Id {}'.format(event, indicator_id, batch_id))
            return False

        # Insert data set event
        with DbOperation('Event') as op:
            event = op.create(eventTypeId=event_type_list[0].id, sessionId=session_list[0].id, content=data_set)

    # Invalid event
    else:
        log.error('Invalid argument event: {}'.format(event))
        return False

    return event
