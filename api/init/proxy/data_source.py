import docker
from proxy import utils


class TestDataSource():
    """Class used to manage execution of custom mutation testDataSource."""

    def build_payload(self):
        """Method used to surcharge payload sent to GraphQL API."""

        return 'mutation testDataSource($dataSourceId: Int!) { testDataSource(input: { dataSourceId: $dataSourceId }) { dataSource { id connectivityStatus } } }'

    def test_data_source(self, authorization: str, response: dict):
        """Method used to run Docker container which tests connectivity to a data source."""

        data_source_id = str(response['data']['testDataSource']['dataSource']['id'])
        container_name = f'mobydq-test-data-source-{data_source_id}'
        client = docker.from_env()
        client.containers.run(
            name=container_name,
            image='mobydq-scripts',
            network='mobydq_network',
            command=['python', 'run.py', authorization, 'test_data_source', data_source_id],
            stream=True,
            remove=True
        )

        # Get connectivity test result
        query = 'query{dataSourceById(id:data_source_id){id,connectivityStatus,updatedDate,userByUpdatedById{email}}}'
        query = query.replace('data_source_id', str(data_source_id))  # Use replace() instead of format() because of curly braces
        query = {'query': query}  # Convert to dictionary
        data = utils.execute_graphql_request(authorization, query)
        return data
