from graphqlapi.interceptors.graphql_base_interceptor import GraphQlRequestInterceptor, GraphQlRequestException
from graphqlapi.batch import execute_batch
from graphql.language.ast import Document


OPERATION_NAME = 'executeBatch'


class ExecuteBatchInterceptor(GraphQlRequestInterceptor):

    def can_handle(self, ast: Document):
        return self._get_execute_batch(ast) != None

    def after_request(self, executed_ast: Document, status: int, response: object):
        if status != 200:
            return

        executed_batch = self._get_execute_batch(executed_ast)
        batch_id_selections = [selection for selection in executed_batch.selection_set.selections if any(
            [sub_selection.name.value == 'id' and selection.name.value == 'batch' for sub_selection in selection.selection_set.selections])]
        if len(batch_id_selections) == 0:
            message = 'Batch Id attribute is mandatory in the payload to be able to trigger the batch execution. Example: {"query": "mutation{executeBatch(input:{indicatorGroupId:1}){batch{id}}}"'
            raise GraphQlRequestException(400, message)

        batch_id = str(response['data']['executeBatch']['batch']['id'])
        execute_batch(batch_id)

    def _get_execute_batch(self, ast: Document):
        results = [[selection for selection in definition.selection_set.selections if selection.name.value == OPERATION_NAME]
                   for definition in ast.definitions]
        if not len(results) == 1 or not len(results[0]) == 1:
            return None
        return results[0][0]
