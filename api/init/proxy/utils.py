import requests
from graphql.parser import GraphQLParser
from proxy.exceptions import RequestException


def validate_graphql_request(payload: str):
    """Method to parse http request payload verify it is a valid GraphQL query or mutation and return a GraphQL document."""

    try:
        return GraphQLParser().parse(payload)
    except Exception:
        raise RequestException(400, 'Invalid GraphQL payload.')


def execute_graphql_request(payload: dict):
    """Method to execute http request on the GraphQL API."""

    url = 'http://graphql:5433/graphql'  # Should be moved to config file
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    status = response.status_code
    data = response.json()

    return status, data
