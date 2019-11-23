import logging
import sys
from datetime import datetime
from scripts import utils

def get_test_case_name():
    """Generate unique name for unit test case."""
    # If not unique enough, replace with an uuid
    test_case_name = 'test ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    return test_case_name

def configure_test_logger():
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_authorization():
    mutation = '''mutation{authenticateUser(input:{userEmail:"admin",userPassword:"admin"}){token}}'''
    mutation = {'query': mutation}  # Convert to dictionary
    response = utils.execute_graphql_request(None, mutation)
    return "Bearer " + response['data']['authenticateUser']['token']
