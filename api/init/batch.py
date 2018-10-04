import docker


class Batch:
    """Batch class."""

    def __init__(self):
        pass

    def execute(self, batch_id):
        container_name = 'mobydq-batch-{batch_id}'.format(
            batch_id=batch_id)
        client = docker.from_env()
        client.containers.run(
            name=container_name,
            image='mobydq-scripts',
            network='mobydq-network',
            command=['python', 'run.py', 'execute_batch', batch_id],
            remove=True,
            detach=True
        )
