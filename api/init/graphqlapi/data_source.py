import docker
import logging
import graphqlapi.utils as utils


def test_data_source(data_source_id):
    container_name = f'mobydq-test-data-source-{data_source_id}'

    client = docker.from_env()
    client.containers.run(
        name=container_name,
        image='mobydq-scripts',
        network='mobydq-network',
        command=['python', 'run.py', 'test_data_source', data_source_id],
        stream=True,
        remove=True
    )

    # Get connectivity test result
    query = '''query {
        dataSourceById(id:data_source_id) {
            id,
            connectivityStatus
        }
    }'''

    query = query.replace('data_source_id', str(
        data_source_id))  # Use replace() instead of format() because of curly braces
    data = utils.execute_graphql_request(query)
    return data
