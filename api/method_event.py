#!/usr/bin/env python
"""Functions related to event objects."""
from database.operation import Operation
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class MethodEvent:
    """Functions called by the API for event objects."""

    def __init__(self, event_type):
        """Initialize class."""
        # Initialize dictionary for error message
        self.error_message = {}

        # Verify event type exists
        event_type_list = Operation('ModelEventType').read(name=event_type)
        if event_type_list:
            self.event_type_id = event_type_list[0].id
            self.event_type = event_type_list[0].name
        else:
            self.error_message['message'] = 'Cannot log event because event type {} does not exist'.format(event_type)
            log.error(self.error_message['message'])
            return self.error_message

    def log_event(self, indicator_id, batch_id, data_set=None):
        """
        Manage session status and event logging for the corresponding data quality indicator. Return event object.

        If event is Start:
        * Insert a new session
        * New session status is set to Running (Id: 1)
        * Insert a new Start event
        * Returns the corresponding event object

        If event is Stop:
        * Terminate an existing running session
        * Existing session status is set to Succeeded (Id: 2)
        * Insert a new Stop event
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

        # Log start event, insert new running session
        if self.event_type_id == 1:
            log.info('Starting session for indicator Id: {}'.format(indicator_id))

            # Insert new running session and start event
            session = Operation('ModelSession').create(indicatorId=indicator_id, batchId=batch_id, statusId=1)
            event = Operation('ModelEvent').create(eventTypeId=self.event_type_id, sessionId=session.id, content=data_set)

        # Log stop event, update running session to succeeded
        elif self.event_type_id == 2:
            log.info('Stoping session for indicator Id: {}'.format(indicator_id))

            # Verify current indicator is running
            session_list = Operation('ModelSession').read(indicatorId=indicator_id, batchId=batch_id, statusId=1)
            if not session_list:
                self.error_message['message'] = '''Cannot log {} event because indicator with Id {}
                 does not have a running session with batch Id {}'''.format(self.event_type, indicator_id, batch_id)
                log.error(self.error_message['message'])
                return self.error_message

            # Insert stop event and terminate running session
            event = Operation('ModelEvent').create(eventTypeId=self.event_type_id, sessionId=session_list[0].id, content=data_set)
            Operation('ModelSession').update(id=session_list[0].id, statusId=2)

        # Log error event, update running session to failed
        elif self.event_type_id == 3:
            log.info('Failing session for indicator Id: {}'.format(indicator_id))

            # Verify current indicator is running
            session_list = Operation('ModelSession').read(indicatorId=indicator_id, batchId=batch_id, statusId=1)
            if not session_list:
                self.error_message['message'] = '''Cannot log {} event because indicator with Id {}
                 does not have a running session with batch Id {}'''.format(self.event_type, indicator_id, batch_id)
                log.error(self.error_message['message'])
                return self.error_message

            # Insert error event and terminate running session
            event = Operation('ModelEvent').create(eventTypeId=self.event_type_id, sessionId=session_list[0].id, content=data_set)
            Operation('ModelSession').update(id=session_list[0].id, statusId=3)

        # Log data set event
        elif self.event_type_id == 4:
            log.info('Logging data set for indicator Id: {}'.format(indicator_id))

            # Verify current indicator is running
            session_list = Operation('ModelSession').read(indicatorId=indicator_id, batchId=batch_id, statusId=1)
            if not session_list:
                self.error_message['message'] = '''Cannot log {} event because indicator with Id {}
                 does not have a running session with batch Id {}'''.format(self.event_type, indicator_id, batch_id)
                log.error(self.error_message['message'])
                return self.error_message

            # Insert data set event
            event = Operation('ModelEvent').create(eventTypeId=self.event_type_id, sessionId=session_list[0].id, content=data_set)

        return event
