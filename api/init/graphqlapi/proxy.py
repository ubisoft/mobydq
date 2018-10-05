import graphqlapi.utils as utils
from graphql.ast import Document
from graphql.parser import GraphQLParser
from graphqlapi.interceptor import ExecuteBatch, TestDataSource, RequestException
from graphqlapi.exceptions import RequestException


interceptors = [
    ExecuteBatch(),
    TestDataSource()
]


def proxy_request(payload: dict):
    graphql_ast = parse_query(payload['query'])

    # Execute request on GraphQL API
    status, data = utils.execute_graphql_request(payload['query'])

    for interceptor in interceptors:
        if interceptor.can_handle(graphql_ast):
            data = interceptor.after_request(graphql_ast, status, data)

    return 200 if status == 200 else 500, data


def parse_query(payload_query: str):
    try:
        return GraphQLParser().parse(payload_query)
    except Exception:
        raise RequestException(400, 'Invalid GraphQL query')
