import graphql
import graphqlapi.utils as utils
from graphqlapi.interceptor import ExecuteBatch, TestDataSource


interceptors = [
    ExecuteBatch(),
    TestDataSource()
]


def proxy_request(payload):
    graphql_ast = graphql.parse(payload['query'])
    handled_interceptors = []
    for interceptor in interceptors:
        if interceptor.can_handle(graphql_ast):
            graphql_ast = interceptor.intercept_ast_before_request(graphql_ast)
            handled_interceptors.append(interceptor)

    graphql_query = graphql.print_ast(graphql_ast)

    # Execute request on GraphQL API
    status, data = utils.execute_graphql_request(graphql_query)

    for handled_interceptor in handled_interceptors:
        data = handled_interceptor.after_request(graphql_ast, status, data)

    return 200 if status == 200 else 500, data
