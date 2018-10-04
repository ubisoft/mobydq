import docker


def execute_batch(batch_id):
    container_name = f'mobydq-batch-{batch_id}'
    client = docker.from_env()
    client.containers.run(
        name=container_name,
        image='mobydq-scripts',
        network='mobydq-network',
        links={'mobydq-graphql': 'mobydq-graphql'},
        command=['python', 'run.py', 'execute_batch', batch_id],
        remove=True,
        detach=True
    )
