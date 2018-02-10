#!/usr/bin/env python
"""Unit test for api module."""
from test import test_utils
from api.database.operation import Operation
from api.batch_method import BatchMethod
import requests
import socket
import unittest


class TestApiModule(unittest.TestCase):
    """Class to execute unit tests for api.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.base_url = 'http://{}:5000/dataquality/api'.format(socket.gethostname())
        self.headers = {'content-type': 'application/json'}
        self.test_case_list = []

    # Batch namespace
    def test_get_batch_owner_list(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)

        # Get batch owner list
        response = requests.get(self.base_url + '/v1/batchowners', headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json), 0)

    def test_post_batch_owner(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name)

    def test_get_batch_owner(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        record_id = response.json()['id']

        # Get batch owner
        response = requests.get(self.base_url + '/v1/batchowners/{}'.format(record_id), headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json[0]['name'], test_case_name)

    def test_put_batch_owner(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name_updated})

        # Update batch owner
        payload = {}
        payload['id'] = int(record_id)
        payload['name'] = test_case_name_updated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name_updated)

    def test_delete_batch_owner(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)

        # Delete batch owner
        response = requests.delete(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_get_batch_owner_batch(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner amd start batch
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        record_id = response.json()['id']
        batch = BatchMethod(record_id).start()

        # Get batch owner batch
        response = requests.get(self.base_url + '/v1/batchowners/{}/batches'.format(record_id), headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json[0]['id'], batch.id)

    # Data source namespace
    def test_get_data_source_list(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})

        # Create data source
        payload = {}
        payload['name'] = test_case_name
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = test_case_name
        payload['login'] = test_case_name
        payload['password'] = test_case_name
        payload = str(payload).replace("'", '"')
        requests.post(self.base_url + '/v1/datasources', headers=self.headers, data=payload)

        # Get data source list
        response = requests.get(self.base_url + '/v1/datasources', headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json), 0)

    def test_post_data_source(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})

        # Create data source
        payload = {}
        payload['name'] = test_case_name
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = test_case_name
        payload['login'] = test_case_name
        payload['password'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/datasources', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name)

    def test_get_data_source(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})

        # Create data source
        payload = {}
        payload['name'] = test_case_name
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = test_case_name
        payload['login'] = test_case_name
        payload['password'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/datasources', headers=self.headers, data=payload)
        record_id = response.json()['id']

        # Get data source
        response = requests.get(self.base_url + '/v1/datasources/{}'.format(record_id), headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json[0]['name'], test_case_name)

    def test_put_data_source(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})

        # Create data source
        payload = {}
        payload['name'] = test_case_name
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = test_case_name
        payload['login'] = test_case_name
        payload['password'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/datasources', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name_updated})

        # Update data source
        payload = {}
        payload['id'] = int(record_id)
        payload['name'] = test_case_name_updated
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = test_case_name_updated
        payload['login'] = test_case_name_updated
        payload['password'] = test_case_name_updated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.base_url + '/v1/datasources', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name_updated)

    def test_delete_data_source(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSource', 'test_case': test_case_name})

        # Create data source
        payload = {}
        payload['name'] = test_case_name
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = test_case_name
        payload['login'] = test_case_name
        payload['password'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/datasources', headers=self.headers, data=payload)

        # Delete data source
        response = requests.delete(self.base_url + '/v1/datasources', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_get_data_source_type_list(self):
        # Get data source type list
        response = requests.get(self.base_url + '/v1/datasourcetypes', headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json), 0)

    def test_post_data_source_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSourceType', 'test_case': test_case_name})

        # Create data source type
        payload = {}
        payload['name'] = test_case_name
        payload['type'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/datasourcetypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name)

    def test_put_data_source_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSourceType', 'test_case': test_case_name})

        # Create data source type
        payload = {}
        payload['name'] = test_case_name
        payload['type'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/datasourcetypes', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSourceType', 'test_case': test_case_name_updated})

        # Update data source type
        payload = {}
        payload['id'] = int(record_id)
        payload['name'] = test_case_name_updated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.base_url + '/v1/datasourcetypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name_updated)

    def test_delete_data_source_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSourceType', 'test_case': test_case_name})

        # Create data source type
        payload = {}
        payload['name'] = test_case_name
        payload['type'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/datasourcetypes', headers=self.headers, data=payload)

        # Delete data source type
        response = requests.delete(self.base_url + '/v1/datasourcetypes', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    # Event namespace
    def test_get_event_type_list(self):
        # Get event type list
        response = requests.get(self.base_url + '/v1/eventtypes', headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json), 0)

    def test_post_event_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'EventType', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/eventtypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name)

    def test_put_event_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'EventType', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/eventtypes', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'EventType', 'test_case': test_case_name_updated})

        # Update event type
        payload = {}
        payload['id'] = int(record_id)
        payload['name'] = test_case_name_updated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.base_url + '/v1/eventtypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name_updated)

    def test_delete_event_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'EventType', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/eventtypes', headers=self.headers, data=payload)

        # Delete event type
        response = requests.delete(self.base_url + '/v1/eventtypes', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    # Indicator namespace
    def test_get_indicator_list(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        batch_owner_id = response.json()['id']

        # Create indicator
        payload = {}
        payload['name'] = test_case_name
        payload['description'] = test_case_name
        payload['indicatorTypeId'] = 1
        payload['batchOwnerId'] = batch_owner_id
        payload['executionOrder'] = 0
        payload['active'] = 1
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/indicators', headers=self.headers, data=payload)
        json = response.json()

        # Get indicator list
        response = requests.get(self.base_url + '/v1/indicators', headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json), 0)

    def test_post_indicator(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        batch_owner_id = response.json()['id']

        # Create indicator
        payload = {}
        payload['name'] = test_case_name
        payload['description'] = test_case_name
        payload['indicatorTypeId'] = 1
        payload['batchOwnerId'] = batch_owner_id
        payload['executionOrder'] = 0
        payload['active'] = 1
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/indicators', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name)

    def test_get_indicator(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        batch_owner_id = response.json()['id']

        # Create indicator
        payload = {}
        payload['name'] = test_case_name
        payload['description'] = test_case_name
        payload['indicatorTypeId'] = 1
        payload['batchOwnerId'] = batch_owner_id
        payload['executionOrder'] = 0
        payload['active'] = 1
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/indicators', headers=self.headers, data=payload)
        record_id = response.json()['id']

        # Get data source
        response = requests.get(self.base_url + '/v1/indicators/{}'.format(record_id), headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json[0]['name'], test_case_name)

    def test_put_indicator(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        batch_owner_id = response.json()['id']

        # Create indicator
        payload = {}
        payload['name'] = test_case_name
        payload['description'] = test_case_name
        payload['indicatorTypeId'] = 1
        payload['batchOwnerId'] = batch_owner_id
        payload['executionOrder'] = 0
        payload['active'] = 1
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/indicators', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name_updated})
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Update indicator
        payload = {}
        payload['id'] = int(record_id)
        payload['name'] = test_case_name_updated
        payload['description'] = test_case_name_updated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.base_url + '/v1/indicators', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name_updated)

    def test_delete_indicator(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})
        self.test_case_list.append({'class': 'Indicator', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        batch_owner_id = response.json()['id']

        # Create indicator
        payload = {}
        payload['name'] = test_case_name
        payload['description'] = test_case_name
        payload['indicatorTypeId'] = 1
        payload['batchOwnerId'] = batch_owner_id
        payload['executionOrder'] = 0
        payload['active'] = 1
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/indicators', headers=self.headers, data=payload)

        # Delete indicator
        response = requests.delete(self.base_url + '/v1/indicators', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_get_indicator_type_list(self):
        # Get indicator type
        response = requests.get(self.base_url + '/v1/indicatortypes', headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json), 0)

    def test_post_indicator_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'IndicatorType', 'test_case': test_case_name})

        # Create indicator type
        payload = {}
        payload['name'] = test_case_name
        payload['module'] = test_case_name
        payload['function'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/indicatortypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name)

    def test_put_indicator_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'IndicatorType', 'test_case': test_case_name})

        # Create indicator type
        payload = {}
        payload['name'] = test_case_name
        payload['module'] = test_case_name
        payload['function'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/indicatortypes', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'IndicatorType', 'test_case': test_case_name_updated})

        # Update indicator type
        payload = {}
        payload['id'] = int(record_id)
        payload['name'] = test_case_name_updated
        payload['module'] = test_case_name_updated
        payload['function'] = test_case_name_updated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.base_url + '/v1/indicatortypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name_updated)

    def test_delete_indicator_type(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'IndicatorType', 'test_case': test_case_name})

        # Create indicator type
        payload = {}
        payload['name'] = test_case_name
        payload['module'] = test_case_name
        payload['function'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/indicatortypes', headers=self.headers, data=payload)

        # Delete indicator type
        response = requests.delete(self.base_url + '/v1/indicatortypes', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    # Status namespace
    def test_get_status_list(self):
        # Get event type
        response = requests.get(self.base_url + '/v1/status', headers=self.headers)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json), 0)

    def test_post_status(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Status', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/status', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name)

    def test_put_status(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Status', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/status', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Status', 'test_case': test_case_name_updated})

        # Update event type
        payload = {}
        payload['id'] = int(record_id)
        payload['name'] = test_case_name_updated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.base_url + '/v1/status', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name_updated)

    def test_delete_status(self):
        test_case_name = test_utils.get_test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Status', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/status', headers=self.headers, data=payload)

        # Delete event type
        response = requests.delete(self.base_url + '/v1/status', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for test_case in self.test_case_list:
            Operation(test_case['class']).delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApiModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
