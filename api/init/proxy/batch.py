import docker


class ExecuteBatch():
    """Class used to manage execution of custom mutation executeBatch."""

    def build_payload(self, mutation_arguments: dict):
        """Method used to surcharge payload sent to GraphQL API."""

        mutation = '''mutation executeBatch{executeBatch(input:mutation_arguments){batch{id,status}}}'''
        mutation = mutation.replace('mutation_arguments', str(mutation_arguments))  # Use replace() instead of format() because of curly braces
        payload = {'query': mutation}
        return payload

    def execute_batch(response: dict):
        """Method used to run Docker container which executes batch of indicators."""

        batch_id = str(response['data']['executeBatch']['batch']['id'])
        container_name = f'mobydq-batch-{batch_id}'
        client = docker.from_env()
        client.containers.run(
            name=container_name,
            image='mobydq-scripts',
            network='mobydq-network',
            command=['python', 'run.py', 'execute_batch', batch_id],
            remove=True,
            detach=True
        )

        # Return original response as container is executed in background
        return response
