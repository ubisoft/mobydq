import docker


def execute_batch(batch_id):
    container_name = 'data-quality-batch-{batch_id}'.format(batch_id=batch_id)
    client = docker.from_env()
    client.containers.run(
        name=container_name,
        image='data-quality-scripts',
        network='data-quality-network',
        links={'data-quality-graphql': 'data-quality-graphql'},
        command=['python', 'run.py', 'execute_batch', batch_id],
        #remove=True,
        detach=True
        )
