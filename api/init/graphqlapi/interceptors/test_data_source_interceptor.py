from graphqlapi.interceptors.graphql_base_interceptor import GraphQlRequestInterceptor


class TestDataSourceInterceptor(GraphQlRequestInterceptor):

    def can_handle(self, ast):
        pass

    def intercept_ast_before_request(self, ast):
        return ast

    def after_request(self, executed_ast, status, response):
        pass
