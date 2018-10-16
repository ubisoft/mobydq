import docker
from proxy import utils


class TestDataSource():
    """Class used to manage execution of custom mutation testDataSource."""

    def build_payload(self, mutation_arguments: str):
        """Method used to surcharge payload sent to GraphQL API."""

        mutation = f'mutation testDataSource{{testDataSource(input:{mutation_arguments}){{dataSource{{id,connectivityStatus}}}}}}'
        return mutation

    def test_data_source(self, response: dict):
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
        query = f'query{{dataSourceById(id:{data_source_id}){{id,connectivityStatus}}}}'
        data = utils.execute_graphql_request(query)
        return data
