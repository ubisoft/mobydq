"""Entrypoint to execute python scripts."""
from batch import Batch
from data_source import DataSource
import argparse
import logging
import sys


log = logging.getLogger(__name__)
logging.basicConfig(
    # filename='mobydq.log',
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Entry point to execute data quality scripts.')
    parser.add_argument('method', type=str, help='Method to be executed.')
    parser.add_argument('id', type=int, help='Id of the object on which to execute the method.')
    arguments = parser.parse_args()

    method = arguments.method
    if method == 'execute_batch':
        batch_id = arguments.id
        batch = Batch()
        batch.execute(batch_id)

    elif method == 'test_data_source':
        data_source_id = arguments.id
        data_source = DataSource()
        data_source.test(data_source_id)

    else:
        error_message = 'Invalid method {method}'.format(method=method)
        log.error(error_message)
        raise Exception(error_message)
