#!/usr/bin/env python
"""Functions related to batch objects."""
from .database.operation import Operation
from .indicator_method import IndicatorMethod
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class BatchMethod:
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
        batch_list = Operation('Batch').create(batchOwnerId=self.batch_owner_id, statusId=1)
        return batch_list

    def stop(self):
        """
        Stop a running batch. Return batch object.
        * Terminate an existing running batch
        * Existing batch status is set to Succeeded (Id: 2)
        * Returns the corresponding batch object
        """
        log.info('Stoping batch for batch owner Id: {}'.format(self.batch_owner_id))
        batch_list = Operation('Batch').read(batchOwnerId=self.batch_owner_id, statusId=1)

        if not batch_list:
            self.error_message['message'] = '''Cannot end batch because batch owner Id {}
             does not have a running batch'''.format(self.batch_owner_id)
            log.error(self.error_message['message'])
            return self.error_message

        # Update running batch
        batch_list = Operation('Batch').update(id=batch_list[0].id, statusId=2)
        return batch_list

    def fail(self):
        """
        Fail a running batch. Return batch object.
        * Terminate an existing running batch
        * Existing batch status is set to Failed (Id: 3)
        * Returns the corresponding batch object
        """
        log.info('Failing batch for batch owner Id: {}'.format(self.batch_owner_id))
        batch_list = Operation('Batch').read(batchOwnerId=self.batch_owner_id, statusId=1)

        if not batch_list:
            self.error_message['message'] = '''Cannot fail batch because batch owner Id {}
             does not have a running batch'''.format(self.batch_owner_id)
            log.error(self.error_message['message'])
            return self.error_message

        # Update running batch
        batch_list = Operation('Batch').update(id=batch_list[0].id, statusId=3)
        return batch_list

    def execute(self, batch_owner_id):
        batch_record = self.start()

        # Get indicators for the batch owner
        indicator_list = Operation('Indicator').read(batchOwnerId=batch_owner_id)

        for indicator_record in indicator_list:
            IndicatorMethod(indicator_record.id).execute(batch_record.id)

        self.stop()
