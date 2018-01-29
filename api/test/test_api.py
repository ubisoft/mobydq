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
        batch_owner = Operation('BatchOwner').create(**batch_owner_data)
        batch_data = {}
        batch_data['batchOwnerId'] = batch_owner.id
        batch_data['statusId'] = 1  # Running
        batch = Operation('Batch').create(**batch_data)

        # Get batch
        batch_global_id = '\\"{}\\"'.format(to_global_id('Batch', batch.id))
        payload = '{"query": "{batch (id:%s) {id batchOwnerId}}"}' % batch_global_id
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
        batch_owner = Operation('BatchOwner').create(**batch_owner_data)
        batch_data = {}
        batch_data['batchOwnerId'] = batch_owner.id
        batch_data['statusId'] = 1  # Running
        Operation('Batch').create(**batch_data)

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
        batch_owner = Operation('BatchOwner').create(**batch_owner_data)

        # Get batch owner
        batch_owner_global_id = '\\"{}\\"'.format(to_global_id('BatchOwner', batch_owner.id))
        payload = '{"query": "{batchOwner (id:%s) {id name}}"}' % batch_owner_global_id
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
        Operation('BatchOwner').create(**batch_owner_data)

        # Get batch owner list
        payload = '{"query": "{batchOwners {edges {node {id}}}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json['data']['batchOwners']['edges']), 0)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApiModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
