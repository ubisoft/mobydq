from graphqlapi.interceptors.graphql_base_interceptor import GraphQlRequestInterceptor
from graphql.language.ast import Document


class TestDataSourceInterceptor(GraphQlRequestInterceptor):

    def can_handle(self, ast: Document):
        pass

    def intercept_ast_before_request(self, ast: Document):
        return ast

    def after_request(self, executed_ast: Document, status: int, response: object):
        pass
