import sys
from graphql.ast import Document
import proxy.batch as batch  # Called dynamically with getattr pylint: disable=W0611
import proxy.data_source as data_source  # Called dynamically with getattr pylint: disable=W0611


class Interceptor():
    """Class used to intercept custom mutations and trigger the corresponding scripts."""

    def __init__(self):
        self.can_handle_mutations = {
            'executeBatch': {'module': 'proxy.batch', 'class': 'ExecuteBatch', 'method': 'execute_batch'},
            'testDataSource': {'module': 'proxy.data_source', 'class': 'TestDataSource', 'method': 'test_data_source'}
        }

    def get_mutation_name(self, payload: Document):
        """Method used to verify if the interceptor can handle the mutation."""

        mutation_name = payload.definitions[0].selections[0].name
        if mutation_name in self.can_handle_mutations:
            return mutation_name
        return None

    def get_mutation_arguments(self, payload: Document):
        """Method used to extract mutation arguments from the original payload."""

        # Rebuild arguments as valid GraphQL string
        arguments_dict = payload.definitions[0].selections[0].arguments[0].value
        arguments_string = ''
        for key, value in arguments_dict.items():
            argument = str(key) + ':' + str(value) + ','
            arguments_string = arguments_string + argument
        arguments_string = '{' + arguments_string[:-1] + '}'

        return arguments_string

    def before_request(self, mutation_name: str, mutation_arguments: dict):
        """Method used to recreate the payload to be sent to GraphQL API."""

        module_name = self.can_handle_mutations[mutation_name]['module']
        class_name = self.can_handle_mutations[mutation_name]['class']
        class_instance = getattr(sys.modules[module_name], class_name)()
        payload = getattr(class_instance, 'build_payload')(mutation_arguments)
        return payload

    def after_request(self, mutation_name: str, response: dict):
        """Method used to trigger scripts after the request to GraphQL API."""

        module_name = self.can_handle_mutations[mutation_name]['module']
        class_name = self.can_handle_mutations[mutation_name]['class']
        method_name = self.can_handle_mutations[mutation_name]['method']
        class_instance = getattr(sys.modules[module_name], class_name)()
        response = getattr(class_instance, method_name)(response)
        return response
