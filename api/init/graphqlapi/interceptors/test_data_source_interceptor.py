from graphqlapi.interceptors.graphql_base_interceptor import GraphQlRequestInterceptor, GraphQlRequestException
from graphqlapi.interceptors.shared.utils import fetch_operation_from_ast, get_subselection
from graphql.language.ast import Document
from graphqlapi.data_source import test_data_source


OPERATION_NAME = 'testDataSource'


class TestDataSourceInterceptor(GraphQlRequestInterceptor):

    def can_handle(self, ast: Document):
        return self._get_test_data_source(ast) != None

    def after_request(self, executed_ast: Document, status: int, response: object):
        if status != 200:
            return response

        if 'id' in response['data']['testDataSource']['dataSource']:
            data_source_id = str(
                response['data']['testDataSource']['dataSource']['id'])
            _, response = test_data_source(data_source_id)
            return response
        else:
            message = "Data Source Id attribute is mandatory in the payload to be able to test the connectivity. Example: {'query': 'mutation{testDataSource(input:{dataSourceId:1}){dataSource{id}}}'"
            raise GraphQlRequestException(400, message)

    def _get_test_data_source(self, ast: Document):
        return fetch_operation_from_ast(ast, OPERATION_NAME)
