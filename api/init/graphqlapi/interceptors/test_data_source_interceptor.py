from graphqlapi.interceptors.graphql_base_interceptor import GraphQlRequestInterceptor
from graphql.language.ast import Document


class TestDataSourceInterceptor(GraphQlRequestInterceptor):

    def can_handle(self, ast: Document):
        pass

    def after_request(self, executed_ast: Document, status: int, response: object):
        if status != 200:
            return




    # # Test connectivity to a data source
    # if status == 200 and 'testDataSource' in payload['query']:
    #     if 'id' in data['data']['testDataSource']['dataSource']:
    #         data_source_id = str(
    #             data['data']['testDataSource']['dataSource']['id'])
    #         data = test_data_source(data_source_id)
    #     else:
    #         message = "Data Source Id attribute is mandatory in the payload to be able to test the connectivity. Example: {'query': 'mutation{testDataSource(input:{dataSourceId:1}){dataSource{id}}}'"
    #         return 400, message
