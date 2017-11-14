#!/usr/bin/env python
"""Controls indicators execution and logs events."""
from api.database.operation import Operation as DbOperation
import argparse
import indicator
import logging
import utils

from api.api_utils import _log_batch

# Load logger
utils.config_logger()
log = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Id', type=int, help='Enter the Id of the batch owner for which you want to run a batch.')
    arguments = parser.parse_args()

    # Start batch
    batch_record = _log_batch(arguments.Id, 'Start')

    # Get indicators for the batch owner
    indicator_list = DbOperation('Indicator').read(batchOwnerId=arguments.Id)

    for indicator_record in indicator_list:
        indicator.execute(indicator_record.id, batch_record.id)

    # Stop batch
    _log_batch(arguments.Id, 'Stop')
