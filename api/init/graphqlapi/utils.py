import requests


def execute_graphql_request(payload: dict):
    """Execute queries and mutations on the GraphQL API."""
    url = 'http://graphql:5433/graphql'  # Should be moved to config file
    headers = {'Content-Type': 'application/graphql'}
    response = requests.post(url, headers=headers, data=payload)
    status = response.status_code
    data = response.json()
    return status, data
