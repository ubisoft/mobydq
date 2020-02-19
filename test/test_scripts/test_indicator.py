"""Unit tests for module /scripts/init/indicator.py."""
import unittest
from shared.utils import get_test_case_name, get_authorization
from scripts.constants import IndicatorType
from scripts.indicator import Indicator
from scripts import utils


class TestIndicator(unittest.TestCase):
    """Unit tests for class Indicator."""

    def test_verify_indicator_parameters_completeness(self):
        """Unit tests for method verify_indicator_parameters for completeness indicators."""

        # Authenticate user
        authorization = get_authorization()

        # Create test indicator group
        test_case_name = get_test_case_name()
        mutation_create_indicator_group = '''mutation{createIndicatorGroup(input:{indicatorGroup:{name:"test_case_name",}}){indicatorGroup{id}}}'''
        mutation_create_indicator_group = mutation_create_indicator_group.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator_group = {'query': mutation_create_indicator_group}  # Convert to dictionary
        indicator_group = utils.execute_graphql_request(authorization, mutation_create_indicator_group)
        indicator_group_id = indicator_group['data']['createIndicatorGroup']['indicatorGroup']['id']

        # Create test indicator
        indicator_type_id = IndicatorType.COMPLETENESS
        mutation_create_indicator = '''mutation{createIndicator(input:{indicator:{name:"test_case_name",flagActive:true,indicatorTypeId:indicator_type_id,indicatorGroupId:indicator_group_id}}){indicator{id}}}'''
        mutation_create_indicator = mutation_create_indicator.replace('indicator_type_id', str(indicator_type_id))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = {'query': mutation_create_indicator}  # Convert to dictionary
        indicator = utils.execute_graphql_request(authorization, mutation_create_indicator)
        indicator_id = indicator['data']['createIndicator']['indicator']['id']

        # Create test indicator parameters
        default_parameters = {
            1: "==",  # Alert operator
            2: "0",  # Alert threshold
            3: "['email_1', 'email_2', 'email_3']",  # Distribution list
            4: "['dimension_1', 'dimension_2', 'dimension_3']",  # Dimension
            5: "['measure_1', 'measure_2', 'measure_3']",  # Measures
            6: "Source",  # Source
            7: "Source request",  # Source request
            8: "Target",  # Target
            9: "Target request"  # Target request
            }

        for param_key, param_value in default_parameters.items():
            mutation_create_parameter = '''mutation{createParameter(input:{parameter:{parameterTypeId:param_key,value:"param_value",indicatorId:indicator_id}}){parameter{id}}}'''
            mutation_create_parameter = mutation_create_parameter.replace('param_key', str(param_key))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = mutation_create_parameter.replace('param_value', str(param_value))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = mutation_create_parameter.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = {'query': mutation_create_parameter}  # Convert to dictionary
            utils.execute_graphql_request(authorization, mutation_create_parameter)

        # Get list of parameters
        query_get_parameters = '''query{indicatorById(id:indicator_id){parametersByIndicatorId{nodes{parameterTypeId,value}}}}'''
        query_get_parameters = query_get_parameters.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
        query_get_parameters = {'query': query_get_parameters}  # Convert to dictionary
        parameters = utils.execute_graphql_request(authorization, query_get_parameters)
        parameters = parameters['data']['indicatorById']['parametersByIndicatorId']['nodes']

        indicator = Indicator()
        verified_parameters = indicator.verify_indicator_parameters(authorization, indicator_type_id, parameters)

        # Assert list of parameters is correct
        self.assertEqual(len(verified_parameters), 9)
        self.assertEqual(len(verified_parameters[3]), 3)
        self.assertEqual(len(verified_parameters[4]), 3)
        self.assertEqual(len(verified_parameters[5]), 3)

    def test_verify_indicator_parameters_freshness(self):
        """Unit tests for method verify_indicator_parameters for freshness indicators."""

        # Authenticate user
        authorization = get_authorization()

        # Create test indicator group
        test_case_name = get_test_case_name()
        mutation_create_indicator_group = '''mutation{createIndicatorGroup(input:{indicatorGroup:{name:"test_case_name",}}){indicatorGroup{id}}}'''
        mutation_create_indicator_group = mutation_create_indicator_group.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator_group = {'query': mutation_create_indicator_group}  # Convert to dictionary
        indicator_group = utils.execute_graphql_request(authorization, mutation_create_indicator_group)
        indicator_group_id = indicator_group['data']['createIndicatorGroup']['indicatorGroup']['id']

        # Create test indicator
        indicator_type_id = IndicatorType.FRESHNESS
        mutation_create_indicator = '''mutation{createIndicator(input:{indicator:{name:"test_case_name",flagActive:true,indicatorTypeId:indicator_type_id,indicatorGroupId:indicator_group_id}}){indicator{id}}}'''
        mutation_create_indicator = mutation_create_indicator.replace('indicator_type_id', str(indicator_type_id))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = {'query': mutation_create_indicator}  # Convert to dictionary
        indicator = utils.execute_graphql_request(authorization, mutation_create_indicator)
        indicator_id = indicator['data']['createIndicator']['indicator']['id']

        # Create test indicator parameters
        default_parameters = {
            1: "==",  # Alert operator
            2: "0",  # Alert threshold
            3: "['email_1', 'email_2', 'email_3']",  # Distribution list
            4: "['dimension_1', 'dimension_2', 'dimension_3']",  # Dimension
            5: "['measure_1', 'measure_2', 'measure_3']",  # Measures
            8: "Target",  # Target
            9: "Target request"  # Target request
            }

        for param_key, param_value in default_parameters.items():
            mutation_create_parameter = '''mutation{createParameter(input:{parameter:{parameterTypeId:param_key,value:"param_value",indicatorId:indicator_id}}){parameter{id}}}'''
            mutation_create_parameter = mutation_create_parameter.replace('param_key', str(param_key))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = mutation_create_parameter.replace('param_value', str(param_value))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = mutation_create_parameter.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = {'query': mutation_create_parameter}  # Convert to dictionary
            utils.execute_graphql_request(authorization, mutation_create_parameter)

        # Get list of parameters
        query_get_parameters = '''query{indicatorById(id:indicator_id){parametersByIndicatorId{nodes{parameterTypeId,value}}}}'''
        query_get_parameters = query_get_parameters.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
        query_get_parameters = {'query': query_get_parameters}  # Convert to dictionary
        parameters = utils.execute_graphql_request(authorization, query_get_parameters)
        parameters = parameters['data']['indicatorById']['parametersByIndicatorId']['nodes']

        indicator = Indicator()
        verified_parameters = indicator.verify_indicator_parameters(authorization, indicator_type_id, parameters)

        # Assert list of parameters is correct
        self.assertEqual(len(verified_parameters), 7)
        self.assertEqual(len(verified_parameters[3]), 3)
        self.assertEqual(len(verified_parameters[4]), 3)
        self.assertEqual(len(verified_parameters[5]), 3)

    def test_verify_indicator_parameters_latency(self):
        """Unit tests for method verify_indicator_parameters for latency indicators."""

        # Authenticate user
        authorization = get_authorization()

        # Create test indicator group
        test_case_name = get_test_case_name()
        mutation_create_indicator_group = '''mutation{createIndicatorGroup(input:{indicatorGroup:{name:"test_case_name",}}){indicatorGroup{id}}}'''
        mutation_create_indicator_group = mutation_create_indicator_group.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator_group = {'query': mutation_create_indicator_group}  # Convert to dictionary
        indicator_group = utils.execute_graphql_request(authorization, mutation_create_indicator_group)
        indicator_group_id = indicator_group['data']['createIndicatorGroup']['indicatorGroup']['id']

        # Create test indicator
        indicator_type_id = IndicatorType.LATENCY
        mutation_create_indicator = '''mutation{createIndicator(input:{indicator:{name:"test_case_name",flagActive:true,indicatorTypeId:indicator_type_id,indicatorGroupId:indicator_group_id}}){indicator{id}}}'''
        mutation_create_indicator = mutation_create_indicator.replace('indicator_type_id', str(indicator_type_id))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = {'query': mutation_create_indicator}  # Convert to dictionary
        indicator = utils.execute_graphql_request(authorization, mutation_create_indicator)
        indicator_id = indicator['data']['createIndicator']['indicator']['id']

        # Create test indicator parameters
        default_parameters = {
            1: "==",  # Alert operator
            2: "0",  # Alert threshold
            3: "['email_1', 'email_2', 'email_3']",  # Distribution list
            4: "['dimension_1', 'dimension_2', 'dimension_3']",  # Dimension
            5: "['measure_1', 'measure_2', 'measure_3']",  # Measures
            6: "Source",  # Source
            7: "Source request",  # Source request
            8: "Target",  # Target
            9: "Target request"  # Target request
            }

        for param_key, param_value in default_parameters.items():
            mutation_create_parameter = '''mutation{createParameter(input:{parameter:{parameterTypeId:param_key,value:"param_value",indicatorId:indicator_id}}){parameter{id}}}'''
            mutation_create_parameter = mutation_create_parameter.replace('param_key', str(param_key))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = mutation_create_parameter.replace('param_value', str(param_value))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = mutation_create_parameter.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = {'query': mutation_create_parameter}  # Convert to dictionary
            utils.execute_graphql_request(authorization, mutation_create_parameter)

        # Get list of parameters
        query_get_parameters = '''query{indicatorById(id:indicator_id){parametersByIndicatorId{nodes{parameterTypeId,value}}}}'''
        query_get_parameters = query_get_parameters.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
        query_get_parameters = {'query': query_get_parameters}  # Convert to dictionary
        parameters = utils.execute_graphql_request(authorization, query_get_parameters)
        parameters = parameters['data']['indicatorById']['parametersByIndicatorId']['nodes']

        indicator = Indicator()
        verified_parameters = indicator.verify_indicator_parameters(authorization, indicator_type_id, parameters)

        # Assert list of parameters is correct
        self.assertEqual(len(verified_parameters), 9)
        self.assertEqual(len(verified_parameters[3]), 3)
        self.assertEqual(len(verified_parameters[4]), 3)
        self.assertEqual(len(verified_parameters[5]), 3)

    def test_verify_indicator_parameters_validity(self):
        """Unit tests for method verify_indicator_parameters for validity indicators."""

        # Authenticate user
        authorization = get_authorization()

        # Create test indicator group
        test_case_name = get_test_case_name()
        mutation_create_indicator_group = '''mutation{createIndicatorGroup(input:{indicatorGroup:{name:"test_case_name",}}){indicatorGroup{id}}}'''
        mutation_create_indicator_group = mutation_create_indicator_group.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator_group = {'query': mutation_create_indicator_group}  # Convert to dictionary
        indicator_group = utils.execute_graphql_request(authorization, mutation_create_indicator_group)
        indicator_group_id = indicator_group['data']['createIndicatorGroup']['indicatorGroup']['id']

        # Create test indicator
        indicator_type_id = IndicatorType.VALIDITY
        mutation_create_indicator = '''mutation{createIndicator(input:{indicator:{name:"test_case_name",flagActive:true,indicatorTypeId:indicator_type_id,indicatorGroupId:indicator_group_id}}){indicator{id}}}'''
        mutation_create_indicator = mutation_create_indicator.replace('indicator_type_id', str(indicator_type_id))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = {'query': mutation_create_indicator}  # Convert to dictionary
        indicator = utils.execute_graphql_request(authorization, mutation_create_indicator)
        indicator_id = indicator['data']['createIndicator']['indicator']['id']

        # Create test indicator parameters
        default_parameters = {
            1: "==",  # Alert operator
            2: "0",  # Alert threshold
            3: "['email_1', 'email_2', 'email_3']",  # Distribution list
            4: "['dimension_1', 'dimension_2', 'dimension_3']",  # Dimension
            5: "['measure_1', 'measure_2', 'measure_3']",  # Measures
            8: "Target",  # Target
            9: "Target request"  # Target request
            }

        for param_key, param_value in default_parameters.items():
            mutation_create_parameter = '''mutation{createParameter(input:{parameter:{parameterTypeId:param_key,value:"param_value",indicatorId:indicator_id}}){parameter{id}}}'''
            mutation_create_parameter = mutation_create_parameter.replace('param_key', str(param_key))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = mutation_create_parameter.replace('param_value', str(param_value))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = mutation_create_parameter.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
            mutation_create_parameter = {'query': mutation_create_parameter}  # Convert to dictionary
            utils.execute_graphql_request(authorization, mutation_create_parameter)

        # Get list of parameters
        query_get_parameters = '''query{indicatorById(id:indicator_id){parametersByIndicatorId{nodes{parameterTypeId,value}}}}'''
        query_get_parameters = query_get_parameters.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
        query_get_parameters = {'query': query_get_parameters}  # Convert to dictionary
        parameters = utils.execute_graphql_request(authorization, query_get_parameters)
        parameters = parameters['data']['indicatorById']['parametersByIndicatorId']['nodes']

        indicator = Indicator()
        verified_parameters = indicator.verify_indicator_parameters(authorization, indicator_type_id, parameters)

        # Assert list of parameters is correct
        self.assertEqual(len(verified_parameters), 7)
        self.assertEqual(len(verified_parameters[3]), 3)
        self.assertEqual(len(verified_parameters[4]), 3)
        self.assertEqual(len(verified_parameters[5]), 3)

    def test_get_data_frame(self):
        """Unit tests for method get_data_frame."""

        # Authenticate user
        authorization = get_authorization()

        # Create data source
        test_case_name = get_test_case_name()
        mutation_create_data_source = '''mutation{createDataSource(input:{dataSource:{name:"test_case_name",connectionString:"driver={PostgreSQL Unicode};server=db-postgresql;port=5432;database=star_wars;",login:"postgres",password:"1234",dataSourceTypeId:7}}){dataSource{name}}}'''
        mutation_create_data_source = mutation_create_data_source.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_data_source = {'query': mutation_create_data_source}  # Convert to dictionary
        data_source = utils.execute_graphql_request(authorization, mutation_create_data_source)
        data_source = data_source['data']['createDataSource']['dataSource']['name']

        # Set parameters and call method
        request = 'SELECT gender, COUNT(id) FROM people GROUP BY gender;'
        dimensions = ['gender']
        measures = ['nb_people']
        indicator = Indicator()
        data_frame = indicator.get_data_frame(authorization, data_source, request, dimensions, measures)

        # Assert data frame is correct
        nb_records = len(data_frame)
        nb_females = data_frame.loc[data_frame['gender'] == 'female', 'nb_people'].item()
        self.assertEqual(nb_records, 5)
        self.assertEqual(nb_females, 19)

    def test_is_alert(self):
        """Unit tests for method is_alert."""

        indicator = Indicator()
        equal = indicator.is_alert('0', '==', '0')
        greater = indicator.is_alert('1', '>', '0')
        greater_equal = indicator.is_alert('1', '>=', '0')
        smaller = indicator.is_alert('0', '<', '1')
        smaller_equal = indicator.is_alert('0', '<=', '1')
        different = indicator.is_alert('1', '!=', '2')

        # Assert expressions
        self.assertTrue(equal)
        self.assertTrue(greater)
        self.assertTrue(greater_equal)
        self.assertTrue(smaller)
        self.assertTrue(smaller_equal)
        self.assertTrue(different)


if __name__ == '__main__':
    unittest.main()
