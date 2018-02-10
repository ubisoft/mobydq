#!/usr/bin/env python
"""Unit test for api module."""
from test import test_utils
from api.database.operation import Operation
from graphql_relay.node.node import to_global_id
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

    def test_query_batch(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner and batch in database
        batch_owner_data = {}
        batch_owner_data['name'] = test_case_name
        batch_owner = Operation('ModelBatchOwner').create(**batch_owner_data)
        batch_data = {}
        batch_data['batchOwnerId'] = batch_owner.id
        batch_data['statusId'] = 1  # Running
        batch = Operation('ModelBatch').create(**batch_data)

        # Get batch
        global_id = '\\"{}\\"'.format(to_global_id('Batch', batch.id))
        payload = '{"query": "{batch (id:%s) {id batchOwnerId}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['data']['batch']['batchOwnerId'], batch.batchOwnerId)

    def test_query_batches(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner and batch in database
        batch_owner_data = {}
        batch_owner_data['name'] = test_case_name
        batch_owner = Operation('ModelBatchOwner').create(**batch_owner_data)
        batch_data = {}
        batch_data['batchOwnerId'] = batch_owner.id
        batch_data['statusId'] = 1  # Running
        Operation('ModelBatch').create(**batch_data)

        # Get batch list
        payload = '{"query": "{batches {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['batches']['edges']), 0)

    def test_query_batch_owner(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner in database
        batch_owner_data = {}
        batch_owner_data['name'] = test_case_name
        batch_owner = Operation('ModelBatchOwner').create(**batch_owner_data)

        # Get batch owner
        global_id = '\\"{}\\"'.format(to_global_id('BatchOwner', batch_owner.id))
        payload = '{"query": "{batchOwner (id:%s) {id name}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['data']['batchOwner']['name'], test_case_name)

    def test_query_batch_owners(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner in database
        batch_owner_data = {}
        batch_owner_data['name'] = test_case_name
        Operation('ModelBatchOwner').create(**batch_owner_data)

        # Get batch owner list
        payload = '{"query": "{batchOwners {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['batchOwners']['edges']), 0)

    def test_query_data_source(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})

        # Create data source in database
        data_source_data = {}
        data_source_data = {}
        data_source_data['name'] = test_case_name
        data_source_data['dataSourceTypeId'] = 1  # Hive
        data_source_data['connectionString'] = test_case_name
        data_source_data['login'] = test_case_name
        data_source_data['password'] = test_case_name
        data_source = Operation('ModelDataSource').create(**data_source_data)

        # Get batch owner
        global_id = '\\"{}\\"'.format(to_global_id('DataSource', data_source.id))
        payload = '{"query": "{dataSource (id:%s) {id name}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['data']['dataSource']['name'], test_case_name)

    def test_query_data_sources(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})

        # Create data source in database
        data_source_data = {}
        data_source_data = {}
        data_source_data['name'] = test_case_name
        data_source_data['dataSourceTypeId'] = 1  # Hive
        data_source_data['connectionString'] = test_case_name
        data_source_data['login'] = test_case_name
        data_source_data['password'] = test_case_name
        Operation('ModelDataSource').create(**data_source_data)

        # Get data source list
        payload = '{"query": "{dataSources {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['dataSources']['edges']), 0)

    def test_query_data_source_type(self):
        # Get data source type
        global_id = '\\"{}\\"'.format(to_global_id('DataSourceType', 1))  # Hive
        payload = '{"query": "{dataSourceType (id:%s) {id name}}"}' % global_id
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['data']['dataSourceType']['name'], 'Hive')

    def test_query_data_source_types(self):
        # Get data source type list
        payload = '{"query": "{dataSourceTypes {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['dataSourceTypes']['edges']), 0)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApiModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
