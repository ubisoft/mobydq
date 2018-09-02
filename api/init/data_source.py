import docker


def test_data_source(data_source_id):
    container_name = 'data-quality-test-data-source-{data_source_id}'.format(data_source_id=data_source_id)
    client = docker.from_env()
    client.containers.run(
        name=container_name,
        image='data-quality-scripts',
        network='data-quality-network',
        links={'data-quality-graphql': 'data-quality-graphql'},
        command=['python', 'run.py', 'test_data_source', data_source_id],
        remove=True,
        detach=True
        )
