import docker
import logging
import utils


# Load logging configuration
log = logging.getLogger(__name__)


class DataSource:
    """Data source class."""

    def __init__(self):
        pass

    def test(self, data_source_id):
        container_name = 'data-quality-test-data-source-{data_source_id}'.format(data_source_id=data_source_id)
        client = docker.from_env()
        client.containers.run(
            name=container_name,
            image='data-quality-scripts',
            network='data-quality-network',
            links={'data-quality-graphql': 'data-quality-graphql'},
            command=['python', 'run.py', 'test_data_source', data_source_id],
            stream=True,
            remove=True
            )

        # Get connectivity test result
        query = '''query{dataSourceById(id:data_source_id){id,connectivityStatus}}'''
        query = query.replace('data_source_id', str(data_source_id))  # Use replace() instead of format() because of curly braces
        data = utils.execute_graphql_request(query)

        return data
