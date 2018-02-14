#!/usr/bin/env python
"""Unit test for api module GraphQL create mutations."""
from test import test_utils
from api.database.operation import Operation
from graphql_relay.node.node import from_global_id, to_global_id
import requests
import socket
import unittest


class TestApiModule(unittest.TestCase):
    """Class to execute unit tests for api.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.base_url = 'http://{}:5000/dataquality/api/graphql'.format(socket.gethostname())
        self.headers = {'content-type': 'application/json'}
        self.test_case_list = []

    def test_mutation_create_batch(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelBatchOwner", "test_case": test_case_name})

        # Create batch owner
        payload = '{"query": "mutation {createBatchOwner (input: {name:\\"%s\\"}) {batchOwner {id}}}"}' % test_case_name
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_owner_id = json['data']['createBatchOwner']['batchOwner']['id']

        # Create batch
        status_id = to_global_id('SchemaStatus', 1)  # Running
        input = '{batchOwnerId:\\"%s\\", statusId: \\"%s\\"}' % (batch_owner_id, status_id)
        payload = '{"query": "mutation {createBatch (input: %s) {batch {batchOwner {name} status {name}}}}"}' % (input)
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_owner_name = json['data']['createBatch']['batch']['batchOwner']['name']
        status_name = json['data']['createBatch']['batch']['status']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(batch_owner_name, test_case_name)
        self.assertEqual(status_name, 'Running')

    def test_mutation_create_batch_owner(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelBatchOwner", "test_case": test_case_name})

        # Create batch owner
        payload = '{"query": "mutation {createBatchOwner (input: {name:\\"%s\\"}) {batchOwner {name}}}"}' % test_case_name
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_owner_name = json['data']['createBatchOwner']['batchOwner']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(batch_owner_name, test_case_name)

    def test_mutation_create_data_source(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelDataSource", "test_case": test_case_name})

        # Create data source
        data_source_type_id = to_global_id('SchemaDataSourceType', 1)  # Hive
        input = '{name:\\"%s\\", dataSourceTypeId: \\"%s\\", connectionString: \\"%s\\", login: \\"%s\\", password: \\"%s\\"}' % (test_case_name, data_source_type_id, test_case_name, test_case_name, test_case_name)
        payload = '{"query": "mutation {createDataSource (input: %s) {dataSource {name}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        data_source_name = json['data']['createDataSource']['dataSource']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_source_name, test_case_name)

    def test_mutation_create_data_source_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelDataSourceType", "test_case": test_case_name})

        # Create data source type
        input = '{name:\\"%s\\", parentType: \\"%s\\"}' % (test_case_name, test_case_name)
        payload = '{"query": "mutation {createDataSourceType (input: %s) {dataSourceType {name}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        data_source_type_name = json['data']['createDataSourceType']['dataSourceType']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_source_type_name, test_case_name)

    def test_mutation_create_event(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelIndicator", "test_case": test_case_name})
        self.test_case_list.append({"class": "ModelBatchOwner", "test_case": test_case_name})

        # Create batch owner
        payload = '{"query": "mutation {createBatchOwner (input: {name:\\"%s\\"}) {batchOwner {id}}}"}' % test_case_name
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_owner_id = json['data']['createBatchOwner']['batchOwner']['id']

        # Create indicator
        indicator_type_id = to_global_id('SchemaIndicatorType', 1)  # Completeness
        input = '{name:\\"%s\\", description:\\"%s\\", indicatorTypeId:\\"%s\\", batchOwnerId:\\"%s\\", executionOrder: 1, active: true}' % (test_case_name, test_case_name, indicator_type_id, batch_owner_id)
        payload = '{"query": "mutation {createIndicator (input: %s) {indicator {id}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_id = json['data']['createIndicator']['indicator']['id']

        # Create batch
        status_id = to_global_id('SchemaStatus', 1)  # Running
        input = '{batchOwnerId:\\"%s\\", statusId: \\"%s\\"}' % (batch_owner_id, status_id)
        payload = '{"query": "mutation {createBatch (input: %s) {batch {id}}}"}' % (input)
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_id = json['data']['createBatch']['batch']['id']

        # Create session
        status_id = to_global_id('SchemaStatus', 1)  # Running
        input = '{indicatorId:\\"%s\\", batchId: \\"%s\\", statusId: \\"%s\\"}' % (indicator_id, batch_id, status_id)
        payload = '{"query": "mutation {createSession (input: %s) {session {id}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        session_id = json['data']['createSession']['session']['id']

        # Create event
        event_type_id = to_global_id('SchemaEventType', 1)  # Start
        input = '{sessionId: \\"%s\\", eventTypeId:\\"%s\\"}' % (session_id, event_type_id)
        payload = '{"query": "mutation {createEvent (input: %s) {event {eventType {name}}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        event_type_name = json['data']['createEvent']['event']['eventType']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(event_type_name, 'Start')

    def test_mutation_create_event_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelEventType", "test_case": test_case_name})

        # Create event type
        payload = '{"query": "mutation {createEventType (input: {name:\\"%s\\"}) {eventType {name}}}"}' % test_case_name
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        event_type_name = json['data']['createEventType']['eventType']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(event_type_name, test_case_name)

    def test_mutation_create_indicator(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelIndicator", "test_case": test_case_name})
        self.test_case_list.append({"class": "ModelBatchOwner", "test_case": test_case_name})

        # Create batch owner
        payload = '{"query": "mutation {createBatchOwner (input: {name:\\"%s\\"}) {batchOwner {id}}}"}' % test_case_name
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_owner_id = json['data']['createBatchOwner']['batchOwner']['id']

        # Create indicator
        indicator_type_id = to_global_id('SchemaIndicatorType', 1)  # Completeness
        input = '{name:\\"%s\\", description:\\"%s\\", indicatorTypeId:\\"%s\\", batchOwnerId:\\"%s\\", executionOrder: 1, active: true}' % (test_case_name, test_case_name, indicator_type_id, batch_owner_id)
        payload = '{"query": "mutation {createIndicator (input: %s) {indicator {name batchOwner {name}}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_name = json['data']['createIndicator']['indicator']['name']
        batch_owner_name = json['data']['createIndicator']['indicator']['batchOwner']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(indicator_name, test_case_name)
        self.assertEqual(batch_owner_name, test_case_name)

    def test_mutation_create_indicator_parameter(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelIndicator", "test_case": test_case_name})
        self.test_case_list.append({"class": "ModelBatchOwner", "test_case": test_case_name})

        # Create batch owner
        payload = '{"query": "mutation {createBatchOwner (input: {name:\\"%s\\"}) {batchOwner {id}}}"}' % test_case_name
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_owner_id = json['data']['createBatchOwner']['batchOwner']['id']

        # Create indicator
        indicator_type_id = to_global_id('SchemaIndicatorType', 1)  # Completeness
        input = '{name:\\"%s\\", description:\\"%s\\", indicatorTypeId:\\"%s\\", batchOwnerId:\\"%s\\", executionOrder: 1, active: true}' % (test_case_name, test_case_name, indicator_type_id, batch_owner_id)
        payload = '{"query": "mutation {createIndicator (input: %s) {indicator {id}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_id = json['data']['createIndicator']['indicator']['id']

        # Create indicator parameter
        indicator_parameter_type_id = to_global_id('SchemaIndicatorParameterType', 1)  # Alert operator
        input = '{indicatorId:\\"%s\\", parameterTypeId:\\"%s\\", value:\\"%s\\"}' % (indicator_id, indicator_parameter_type_id, test_case_name)
        payload = '{"query": "mutation {createIndicatorParameter (input: %s) {parameter {value parameterType {name}}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        parameter_value = json['data']['createIndicatorParameter']['parameter']['value']
        parameter_type_name = json['data']['createIndicatorParameter']['parameter']['parameterType']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(parameter_value, test_case_name)
        self.assertEqual(parameter_type_name, 'Alert operator')

    def test_mutation_create_indicator_parameter_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelIndicatorParameterType", "test_case": test_case_name})

        # Create parameter type
        input = '{name:\\"%s\\", description:\\"%s\\"}' % (test_case_name, test_case_name)
        payload = '{"query": "mutation {createIndicatorParameterType (input: %s) {parameterType {name}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        parameter_type_name = json['data']['createIndicatorParameterType']['parameterType']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(parameter_type_name, test_case_name)

    def test_mutation_create_indicator_result(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelIndicator", "test_case": test_case_name})
        self.test_case_list.append({"class": "ModelBatchOwner", "test_case": test_case_name})

        # Create batch owner
        payload = '{"query": "mutation {createBatchOwner (input: {name:\\"%s\\"}) {batchOwner {id}}}"}' % test_case_name
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_owner_id = json['data']['createBatchOwner']['batchOwner']['id']

        # Create indicator
        indicator_type_id = to_global_id('SchemaIndicatorType', 1)  # Completeness
        input = '{name:\\"%s\\", description:\\"%s\\", indicatorTypeId:\\"%s\\", batchOwnerId:\\"%s\\", executionOrder: 1, active: true}' % (test_case_name, test_case_name, indicator_type_id, batch_owner_id)
        payload = '{"query": "mutation {createIndicator (input: %s) {indicator {id}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_id = json['data']['createIndicator']['indicator']['id']

        # Create batch
        status_id = to_global_id('SchemaStatus', 1)  # Running
        input = '{batchOwnerId:\\"%s\\", statusId: \\"%s\\"}' % (batch_owner_id, status_id)
        payload = '{"query": "mutation {createBatch (input: %s) {batch {id}}}"}' % (input)
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_id = json['data']['createBatch']['batch']['id']

        # Create session
        status_id = to_global_id('SchemaStatus', 1)  # Running
        input = '{indicatorId:\\"%s\\", batchId: \\"%s\\", statusId: \\"%s\\"}' % (indicator_id, batch_id, status_id)
        payload = '{"query": "mutation {createSession (input: %s) {session {id}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        session_id = json['data']['createSession']['session']['id']

        # Create indicator result
        input = '{indicatorId:\\"%s\\", sessionId:\\"%s\\", alertOperator:\\"=\\", alertThreshold:0.0, nbRecords:0, nbRecordsAlert:0, nbRecordsNoAlert:0}' % (indicator_id, session_id)
        payload = '{"query": "mutation {createIndicatorResult (input: %s) {indicatorResult {indicator {name} session {batch {batchOwner {name}}}}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_name = json['data']['createIndicatorResult']['indicatorResult']['indicator']['name']
        batch_owner_name = json['data']['createIndicatorResult']['indicatorResult']['session']['batch']['batchOwner']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(indicator_name, test_case_name)
        self.assertEqual(batch_owner_name, test_case_name)

    def test_mutation_create_indicator_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelIndicatorType", "test_case": test_case_name})

        # Create indicator type
        input = '{name:\\"%s\\", function:\\"%s\\"}' % (test_case_name, test_case_name)
        payload = '{"query": "mutation {createIndicatorType (input: %s) {indicatorType {name}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_type_name = json['data']['createIndicatorType']['indicatorType']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(indicator_type_name, test_case_name)

    def test_mutation_create_session(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelIndicator", "test_case": test_case_name})
        self.test_case_list.append({"class": "ModelBatchOwner", "test_case": test_case_name})

        # Create batch owner
        payload = '{"query": "mutation {createBatchOwner (input: {name:\\"%s\\"}) {batchOwner {id}}}"}' % test_case_name
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_owner_id = json['data']['createBatchOwner']['batchOwner']['id']

        # Create indicator
        indicator_type_id = to_global_id('SchemaIndicatorType', 1)  # Completeness
        input = '{name:\\"%s\\", description:\\"%s\\", indicatorTypeId:\\"%s\\", batchOwnerId:\\"%s\\", executionOrder: 1, active: true}' % (test_case_name, test_case_name, indicator_type_id, batch_owner_id)
        payload = '{"query": "mutation {createIndicator (input: %s) {indicator {id}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_id = json['data']['createIndicator']['indicator']['id']

        # Create batch
        status_id = to_global_id('SchemaStatus', 1)  # Running
        input = '{batchOwnerId:\\"%s\\", statusId: \\"%s\\"}' % (batch_owner_id, status_id)
        payload = '{"query": "mutation {createBatch (input: %s) {batch {id}}}"}' % (input)
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_id = json['data']['createBatch']['batch']['id']

        # Create session
        status_id = to_global_id('SchemaStatus', 1)  # Running
        input = '{indicatorId:\\"%s\\", batchId: \\"%s\\", statusId: \\"%s\\"}' % (indicator_id, batch_id, status_id)
        payload = '{"query": "mutation {createSession (input: %s) {session {indicator {name} batch {batchOwner {name}}}}}"}' % input
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_name = json['data']['createSession']['session']['indicator']['name']
        batch_owner_name = json['data']['createSession']['session']['batch']['batchOwner']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(indicator_name, test_case_name)
        self.assertEqual(batch_owner_name, test_case_name)

    def test_mutation_create_status(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({"class": "ModelStatus", "test_case": test_case_name})

        # Create status
        payload = '{"query": "mutation {createStatus (input: {name:\\"%s\\"}) {status {name}}}"}' % test_case_name
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        status_name = json['data']['createStatus']['status']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(status_name, test_case_name)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApiModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
