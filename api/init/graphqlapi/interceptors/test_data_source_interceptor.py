from graphqlapi.interceptors.graphql_base_interceptor import GraphQlRequestInterceptor
from graphql.language.ast import Document


class TestDataSourceInterceptor(GraphQlRequestInterceptor):

    def can_handle(self, ast: Document):
        pass

    def after_request(self, executed_ast: Document, status: int, response: object):
        if status != 200:
            return
