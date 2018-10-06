import docker
import proxy.utils as utils


class TestDataSource():
    """Class used to manage execution of custom mutation testDataSource."""

    def build_payload(self, mutation_arguments: dict):
        """Method used to surcharge payload sent to GraphQL API."""

        mutation = '''mutation testDataSource{testDataSource(input:mutation_arguments){dataSource{id,connectivityStatus}}}'''
        mutation = mutation.replace('mutation_arguments', str(mutation_arguments))  # Use replace() instead of format() because of curly braces
        payload = {'query': mutation}
        return payload

    def test_data_source(response: dict):
        """Method used to run Docker container which tests connectivity to a data source."""

        data_source_id = str(response['data']['testDataSource']['dataSource']['id'])
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
        query = '''query{dataSourceById(id:data_source_id){id,connectivityStatus}}'''
        query = query.replace('data_source_id', str(data_source_id))  # Use replace() instead of format() because of curly braces
        data = utils.execute_graphql_request(query)
        return data
