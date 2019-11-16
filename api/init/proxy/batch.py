import docker


class ExecuteBatch():
    """Class used to manage execution of custom mutation executeBatch."""

    def build_payload(self):
        """Method used to surcharge payload sent to GraphQL API."""

        return 'mutation executeBatch($indicatorGroupId: Int, $indicatorId: [Int]) { executeBatch(input: {indicatorGroupId: $indicatorGroupId, indicatorId: $indicatorId}) { batch { id status }}}'

    def execute_batch(self, authorization: str, response: dict):
        """Method used to run Docker container which executes batch of indicators."""

        batch_id = str(response['data']['executeBatch']['batch']['id'])
        container_name = f'mobydq-batch-{batch_id}'
        client = docker.from_env()
        client.containers.run(
            name=container_name,
            image='mobydq-scripts',
            network='mobydq_network',
            command=['python', 'run.py', authorization, 'execute_batch', batch_id],
            remove=True,
            detach=True
        )

        # Return original response as container is executed in background
        return response
