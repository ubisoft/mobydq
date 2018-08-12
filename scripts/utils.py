import requests


def execute_graphql_request(payload):
    """Execute queries and mutations on the GraphQL API."""
    url = 'http://graphql:5433/graphql'  # Should be moved to config file
    headers = {'Content-Type': 'application/graphql'}
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    return data


def update_batch_status(batch_id, batch_status):
    """Update a batch status."""
    mutation = '''mutation{updateBatchById(input:{id:batch_id,batchPatch:{status:"batch_status"}}){batch{status}}}'''
    mutation = mutation.replace('batch_id', str(batch_id))  # Use replace() instead of format() because of curly braces
    mutation = mutation.replace('batch_status', str(batch_status))  # Use replace() instead of format() because of curly braces
    data = execute_graphql_request(mutation)
    return data
