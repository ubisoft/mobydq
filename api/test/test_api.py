#!/usr/bin/env python
"""Unit test for database module."""
import test_api_utils
import database
import requests
import socket
import unittest
from test import test_utils


class TestApiModule(unittest.TestCase):
    """Class to execute unit tests for api.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.base_url = 'http://{}:5000/dataquality/api'.format(socket.gethostname())
        self.headers = {'content-type': 'application/json'}
        self.test_case_list = []

    def test_post_batch_owner(self):
        """Test post batch owner."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
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
        """Test get batch owner."""
        # Get batch owner
        response = requests.get(self.base_url + '/v1/batchowners', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_batch_owner(self):
        """Test put batch owner."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.test_case_name(self.test_case_list)
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
        """Test delete batch owner."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)

        # Delete batch owner
        response = requests.delete(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_post_batch(self):
        """Test post batch."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'BatchOwner', 'test_case': test_case_name})

        # Create batch owner
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners', headers=self.headers, data=payload)
        batch_owner_id = response.json()['id']

        # Start batch
        payload = {}
        payload['event'] = 'Start'
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/batchowners/{}/batches'.format(batch_owner_id), headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_post_data_source(self):
        """Test post data source."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
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
        """Test get data source."""
        # Get data source
        response = requests.get(self.base_url + '/v1/datasources', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_data_source(self):
        """Test put data source."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
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

        test_case_name_updated = test_utils.test_case_name(self.test_case_list)
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
        """Test delete data source."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
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

    def test_post_data_source_type(self):
        """Test post data source type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
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

    def test_get_data_source_type(self):
        """Test get data source type."""
        # Get data source type
        response = requests.get(self.base_url + '/v1/datasourcetypes', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_data_source_type(self):
        """Test put data source type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'DataSourceType', 'test_case': test_case_name})

        # Create data source type
        payload = {}
        payload['name'] = test_case_name
        payload['type'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/datasourcetypes', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.test_case_name(self.test_case_list)
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
        """Test delete data source type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
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

    def test_post_event_type(self):
        """Test post event type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'EventType', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/eventtypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name)

    def test_get_event_type(self):
        """Test get event type."""
        # Get event type
        response = requests.get(self.base_url + '/v1/eventtypes', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_event_type(self):
        """Test put event type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'EventType', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/eventtypes', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.test_case_name(self.test_case_list)
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
        """Test delete event type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'EventType', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/eventtypes', headers=self.headers, data=payload)

        # Delete event type
        response = requests.delete(self.base_url + '/v1/eventtypes', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_post_indicator_type(self):
        """Test post indicator type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
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

    def test_get_indicatortype(self):
        """Test get indicator type."""
        # Get indicator type
        response = requests.get(self.base_url + '/v1/indicatortypes', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_indicator_type(self):
        """Test put indicator type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'IndicatorType', 'test_case': test_case_name})

        # Create indicator type
        payload = {}
        payload['name'] = test_case_name
        payload['module'] = test_case_name
        payload['function'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/indicatortypes', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.test_case_name(self.test_case_list)
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
        """Test delete indicator type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
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

    def test_post_status(self):
        """Test post event type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Status', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/status', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], test_case_name)

    def test_get_status(self):
        """Test get event type."""
        # Get event type
        response = requests.get(self.base_url + '/v1/status', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_status(self):
        """Test put event type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
        self.test_case_list.append({'class': 'Status', 'test_case': test_case_name})

        # Create event type
        payload = {}
        payload['name'] = test_case_name
        payload = str(payload).replace("'", '"')
        response = requests.post(self.base_url + '/v1/status', headers=self.headers, data=payload)
        record_id = response.json()['id']

        test_case_name_updated = test_utils.test_case_name(self.test_case_list)
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
        """Test delete event type."""
        test_case_name = test_utils.test_case_name(self.test_case_list)
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
            with database.DbOperation(test_case['class']) as op:
                op.delete(name=test_case['test_case'])


if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApiModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
