#!/usr/bin/env python
"""Unit test for api module GraphQL queries."""
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
        self.test_case_name = test_utils.get_test_case_name([])
        self.test_case_list = [self.test_case_name]

        # Create test data set for subsequent query test cases
        # Create data source
        data_source_data = {}
        data_source_data['name'] = self.test_case_name
        data_source_data['dataSourceTypeId'] = 1  # Hive
        data_source_data['connectionString'] = self.test_case_name
        data_source_data['login'] = self.test_case_name
        data_source_data['password'] = self.test_case_name
        self.data_source = Operation('ModelDataSource').create(**data_source_data)

        # Create batch owner
        batch_owner_data = {}
        batch_owner_data['name'] = self.test_case_name
        self.batch_owner = Operation('ModelBatchOwner').create(**batch_owner_data)

        # Create indicator
        indicator_data = {}
        indicator_data['name'] = self.test_case_name
        indicator_data['description'] = self.test_case_name
        indicator_data['indicatorTypeId'] = 1  # Completeness
        indicator_data['batchOwnerId'] = self.batch_owner.id
        indicator_data['executionOrder'] = 1
        indicator_data['active'] = True
        self.indicator = Operation('ModelIndicator').create(**indicator_data)

        # Create indicator parameter
        parameter_data = {}
        parameter_data['indicatorId'] = self.indicator.id
        parameter_data['parameterTypeId'] = 6  # Target request
        parameter_data['value'] = self.test_case_name
        self.parameter = Operation('ModelIndicatorParameter').create(**parameter_data)

        # Create batch
        batch_data = {}
        batch_data['batchOwnerId'] = self.batch_owner.id
        batch_data['statusId'] = 1  # Running
        self.batch = Operation('ModelBatch').create(**batch_data)

        # Create session
        session_data = {}
        session_data['indicatorId'] = self.indicator.id
        session_data['batchId'] = self.batch.id
        session_data['statusId'] = 1  # Running
        self.session = Operation('ModelSession').create(**session_data)

        # Create event
        event_data = {}
        event_data['sessionId'] = self.session.id
        event_data['eventTypeId'] = 1  # Start
        self.event = Operation('ModelEvent').create(**event_data)

        # Create indicator result
        result_data = {}
        result_data['indicatorId'] = self.indicator.id
        result_data['sessionId'] = self.session.id
        result_data['alertOperator'] = '='
        result_data['alertThreshold'] = 0
        result_data['nbRecords'] = 0
        result_data['nbRecordsAlert'] = 0
        result_data['nbRecordsNoAlert'] = 0
        self.result = Operation('ModelIndicatorResult').create(**result_data)

    def test_query_batch(self):
        # Get batch
        global_id = '\\"{}\\"'.format(to_global_id('SchemaBatch', self.batch.id))
        payload = '{"query": "{batch (id:%s) {id}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_id = from_global_id(json['data']['batch']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(batch_id), self.batch.id)

    def test_query_batches(self):
        # Get batch list
        payload = '{"query": "{batches {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['batches']['edges']), 0)

    def test_query_batch_owner(self):
        # Get batch owner
        global_id = '\\"{}\\"'.format(to_global_id('SchemaBatchOwner', self.batch_owner.id))
        payload = '{"query": "{batchOwner (id:%s) {id name}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        batch_owner_id = from_global_id(json['data']['batchOwner']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(batch_owner_id), self.batch_owner.id)

    def test_query_batch_owners(self):
        # Get batch owner list
        payload = '{"query": "{batchOwners {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['batchOwners']['edges']), 0)

    def test_query_data_source(self):
        # Get data source
        global_id = '\\"{}\\"'.format(to_global_id('SchemaDataSource', self.data_source.id))
        payload = '{"query": "{dataSource (id:%s) {id name}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        data_source_id = from_global_id(json['data']['dataSource']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(data_source_id), self.data_source.id)

    def test_query_data_sources(self):
        # Get data source list
        payload = '{"query": "{dataSources {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['dataSources']['edges']), 0)

    def test_query_data_source_type(self):
        # Get data source type
        global_id = '\\"{}\\"'.format(to_global_id('SchemaDataSourceType', 1))  # Hive
        payload = '{"query": "{dataSourceType (id:%s) {id name}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        data_source_type = json['data']['dataSourceType']['name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_source_type, 'Hive')

    def test_query_data_source_types(self):
        # Get data source type list
        payload = '{"query": "{dataSourceTypes {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['dataSourceTypes']['edges']), 0)

    def test_query_event(self):
        # Get event
        global_id = '\\"{}\\"'.format(to_global_id('SchemaEvent', self.event.id))
        payload = '{"query": "{event (id:%s) {id}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        event_id = from_global_id(json['data']['event']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(event_id), self.event.id)

    def test_query_events(self):
        # Get event list
        payload = '{"query": "{events {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['events']['edges']), 0)

    def test_query_indicator(self):
        # Get indicator
        global_id = '\\"{}\\"'.format(to_global_id('SchemaIndicator', self.indicator.id))
        payload = '{"query": "{indicator (id:%s) {id}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_id = from_global_id(json['data']['indicator']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(indicator_id), self.indicator.id)

    def test_query_indicators(self):
        # Get indicator list
        payload = '{"query": "{indicators {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['indicators']['edges']), 0)

    def test_query_indicator_parameter(self):
        # Get indicator parameter
        global_id = '\\"{}\\"'.format(to_global_id('SchemaIndicatorParameter', self.parameter.id))
        payload = '{"query": "{indicatorParameter (id:%s) {id}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        parameter_id = from_global_id(json['data']['indicatorParameter']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(parameter_id), self.parameter.id)

    def test_query_indicator_parameters(self):
        # Get indicator parameter list
        payload = '{"query": "{indicatorParameters {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['indicatorParameters']['edges']), 0)

    def test_query_indicator_parameter_type(self):
        # Get indicator parameter tyoe
        global_id = '\\"{}\\"'.format(to_global_id('SchemaIndicatorParameterType', 1))  # Alert operator
        payload = '{"query": "{indicatorParameterType (id:%s) {id}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        parameter_type_id = from_global_id(json['data']['indicatorParameterType']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(parameter_type_id), 1)  # Alert operator

    def test_query_indicator_parameter_types(self):
        # Get indicator parameter type list
        payload = '{"query": "{indicatorParameterTypes {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['indicatorParameterTypes']['edges']), 0)

    def test_query_indicator_result(self):
        # Get indicator result
        global_id = '\\"{}\\"'.format(to_global_id('SchemaIndicatorResult', self.result.id))
        payload = '{"query": "{indicatorResult (id:%s) {id}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        result_id = from_global_id(json['data']['indicatorResult']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(result_id), self.result.id)

    def test_query_indicator_results(self):
        # Get indicator result list
        payload = '{"query": "{indicatorResults {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['indicatorResults']['edges']), 0)

    def test_query_indicator_type(self):
        # Get indicator type
        global_id = '\\"{}\\"'.format(to_global_id('SchemaIndicatorType', 1))  # Completeness
        payload = '{"query": "{indicatorType (id:%s) {id}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        indicator_type_id = from_global_id(json['data']['indicatorType']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(indicator_type_id), 1)  # Completeness

    def test_query_indicator_types(self):
        # Get indicator type list
        payload = '{"query": "{indicatorTypes {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['indicatorTypes']['edges']), 0)

    def test_query_session(self):
        # Get session
        global_id = '\\"{}\\"'.format(to_global_id('SchemaSession', self.session.id))  # Completeness
        payload = '{"query": "{session (id:%s) {id}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        session_id = from_global_id(json['data']['session']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(session_id), self.session.id)  # Completeness

    def test_query_sessions(self):
        # Get session list
        payload = '{"query": "{sessions {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['sessions']['edges']), 0)

    def test_query_status(self):
        # Get indicator type
        global_id = '\\"{}\\"'.format(to_global_id('SchemaStatus', 1))  # Running
        payload = '{"query": "{status (id:%s) {id}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()
        status_id = from_global_id(json['data']['status']['id'])[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(status_id), 1)  # Running

    def test_query_statuses(self):
        # Get indicator type list
        payload = '{"query": "{statuses {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['statuses']['edges']), 0)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation('ModelDataSource').delete(name=test_case)
            Operation('ModelIndicator').delete(name=test_case)
            Operation('ModelBatchOwner').delete(name=test_case)


if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApiModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
