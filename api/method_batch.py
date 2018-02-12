#!/usr/bin/env python
"""Functions related to batch objects."""
from database.operation import Operation
from method_indicator import MethodIndicator
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class MethodBatch:
    """Functions called by the API for batch objects."""

    def __init__(self, batch_owner_id):
        """Initialize class."""
        # Initialize dictionary for error message
        self.error_message = {}

        # Verify batch owner exists
        batch_owner_list = Operation('BatchOwner').read(id=batch_owner_id)
        if batch_owner_list:
            self.batch_owner_id = batch_owner_list[0].id
        else:
            self.error_message['message'] = 'Batch owner with Id {} does not exist'.format(batch_owner_id)
            log.error(self.error_message['message'])
            return self.error_message

    def start(self):
        """
        Start a new batch. Return batch object.
        * Insert a new batch
        * New batch status is set to Running (Id: 1)
        * Returns the corresponding batch object
        """
        log.info('Starting batch for batch owner Id: {}'.format(self.batch_owner_id))
        batch = Operation('Batch').create(batchOwnerId=self.batch_owner_id, statusId=1)
        return batch

    def stop(self, batch_id):
        """
        Stop a running batch. Return batch object.
        * Terminate an existing running batch
        * Existing batch status is set to Succeeded (Id: 2)
        * Returns the corresponding batch object
        """
        log.info('Stoping batch for batch owner Id: {}'.format(self.batch_owner_id))
        batch_list = Operation('Batch').read(id=batch_id, statusId=1)

        if not batch_list:
            self.error_message['message'] = 'Cannot end batch because batch with Id {} is not running'.format(batch_id)
            log.error(self.error_message['message'])
            return self.error_message

        # Update running batch
        batch = Operation('Batch').update(id=batch_id, statusId=2)
        return batch

    def fail(self, batch_id):
        """
        Fail a running batch. Return batch object.
        * Terminate an existing running batch
        * Existing batch status is set to Failed (Id: 3)
        * Returns the corresponding batch object
        """
        log.info('Failing batch for batch owner Id: {}'.format(self.batch_owner_id))
        batch_list = Operation('Batch').read(id=batch_id, statusId=1)

        if not batch_list:
            self.error_message['message'] = 'Cannot fail batch because batch with Id {} is not running'.format(batch_id)
            log.error(self.error_message['message'])
            return self.error_message

        # Update running batch
        batch = Operation('Batch').update(id=batch_id, statusId=3)
        return batch

    def execute(self, indicator_id=None):
        batch_record = self.start()

        # Get indicators for the batch owner
        if indicator_id is not None:
            indicator_list = Operation('Indicator').read(id=indicator_id, batchOwnerId=self.batch_owner_id)
        else:
            indicator_list = Operation('Indicator').read(batchOwnerId=self.batch_owner_id)

        for indicator_record in indicator_list:
            MethodIndicator(indicator_record.id).execute(batch_record.id)

        self.stop(batch_record.id)
        self.error_message['message'] = 'Batch with Id {} completed successfully'.format(batch_record.id)
        log.info(self.error_message['message'])
        return self.error_message
