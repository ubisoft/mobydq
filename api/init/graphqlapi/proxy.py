import graphql
import graphqlapi.utils as utils
from graphqlapi.data_source import test_data_source
from graphqlapi.interceptors import ExecuteBatchInterceptor, TestDataSourceInterceptor


interceptors = [
    ExecuteBatchInterceptor(),
    TestDataSourceInterceptor()
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
        handled_interceptor.after_request(graphql_ast, status, data)

    # # Test connectivity to a data source
    # if status == 200 and 'testDataSource' in payload['query']:
    #     if 'id' in data['data']['testDataSource']['dataSource']:
    #         data_source_id = str(
    #             data['data']['testDataSource']['dataSource']['id'])
    #         data = test_data_source(data_source_id)
    #     else:
    #         message = "Data Source Id attribute is mandatory in the payload to be able to test the connectivity. Example: {'query': 'mutation{testDataSource(input:{dataSourceId:1}){dataSource{id}}}'"
    #         return 400, message

    return 200 if status == 200 else 500, data
