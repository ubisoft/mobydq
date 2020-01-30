"""Entrypoint to execute python scripts."""
import argparse
import logging
from batch import Batch
from data_source import DataSource
from utils import CustomLogHandler


# Load default logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Entry point to execute data quality scripts.')
    parser.add_argument('authorization', type=str, help='Authentication token of the user')
    parser.add_argument('method', type=str, help='Method to be executed: execute_batch, test_data_source')
    parser.add_argument('id', type=int, help='Id of the object on which to execute the method.')
    arguments = parser.parse_args()

    authorization = arguments.authorization
    method = arguments.method

    if method == 'execute_batch':
        batch_id = arguments.id

        # Customize logger to send logs to GraphQL API when executing a batch
        root_log = logging.getLogger()
        root_log.addHandler(CustomLogHandler(authorization, batch_id=batch_id))

        batch = Batch()
        batch.execute(authorization, batch_id)

    elif method == 'test_data_source':
        data_source_id = arguments.id

        # Customize logger to send logs to GraphQL API when testing a data source
        root_log = logging.getLogger()
        root_log.addHandler(CustomLogHandler(authorization, data_source_id=data_source_id))

        data_source = DataSource()
        data_source.test(authorization, data_source_id)

    else:
        error_message = f'Invalid method {method}'
        log.error(error_message)
        raise Exception(error_message)
