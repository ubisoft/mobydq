import docker


def execute_batch(batch_id: int):
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