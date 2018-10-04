from graphqlapi.interceptors.graphql_base_interceptor import GraphQlRequestInterceptor, GraphQlRequestException
from graphqlapi.batch import execute_batch
from graphqlapi.interceptors.shared.utils import fetch_operation_from_ast, get_subselection
from graphql.language.ast import Document


OPERATION_NAME = 'executeBatch'


class ExecuteBatchInterceptor(GraphQlRequestInterceptor):

    def can_handle(self, ast: Document):
        return self._get_execute_batch(ast) != None

    def after_request(self, executed_ast: Document, status: int, response: object):
        if status != 200:
            return response

        executed_batch = self._get_execute_batch(executed_ast)
        batch_id_selections = get_subselection(executed_batch, 'id', 'batch')
        if len(batch_id_selections) == 0:
            message = 'Batch Id attribute is mandatory in the payload to be able to trigger the batch execution. Example: {"query": "mutation{executeBatch(input:{indicatorGroupId:1}){batch{id}}}"'
            raise GraphQlRequestException(400, message)

        batch_id = str(response['data']['executeBatch']['batch']['id'])
        execute_batch(batch_id)
        return response

    def _get_execute_batch(self, ast: Document):
        return fetch_operation_from_ast(ast, OPERATION_NAME)
