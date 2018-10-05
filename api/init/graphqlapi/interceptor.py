from abc import ABC, abstractmethod
from graphql.ast import Document
from graphqlapi.batch import execute_batch
from graphqlapi.data_source import test_data_source
from graphqlapi.exceptions import RequestException


def fetch_operation_from_ast(ast: Document, operation_name: str):
    results = [[selection for selection in definition.selections if selection.name == operation_name]
               for definition in ast.definitions]
    if not len(results) == 1 or not len(results[0]) == 1:
        return None
    return results[0][0]


def get_subselection(base_selection, name, parent_name):
    sub_selections = [selection for selection in base_selection.selections if any(
        [sub_selection.name == name and selection.name == parent_name for sub_selection in selection.selections])]
    return sub_selections


class BaseRequest(ABC):

    @abstractmethod
    def can_handle(self, ast: Document):
        pass

    @abstractmethod
    def after_request(self, executed_ast: Document, status: int, response: object):
        return response


class ExecuteBatch(BaseRequest):

    def can_handle(self, ast: Document):
        return self._get_execute_batch(ast) != None

    def after_request(self, executed_ast: Document, status: int, response: object):
        if status != 200:
            return response

        executed_batch = self._get_execute_batch(executed_ast)
        batch_id_selections = get_subselection(executed_batch, 'id', 'batch')
        if len(batch_id_selections) == 0:
            message = 'Batch Id attribute is mandatory in the payload to be able to trigger the batch execution. Example: {"query": "mutation{executeBatch(input:{indicatorGroupId:1}){batch{id}}}"'
            raise RequestException(400, message)

        batch_id = str(response['data']['executeBatch']['batch']['id'])
        execute_batch(batch_id)
        return response

    def _get_execute_batch(self, ast: Document):
        return fetch_operation_from_ast(ast, 'executeBatch')


class TestDataSource(BaseRequest):

    def can_handle(self, ast: Document):
        return fetch_operation_from_ast(ast, 'testDataSource') != None

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
            raise RequestException(400, message)
