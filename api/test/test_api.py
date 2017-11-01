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
        self.baseurl = 'http://{}:5000/dataquality/api'.format(socket.gethostname())
        self.headers = {'content-type': 'application/json'}
        self.testcaselist = []

    def test_post_batchowner(self):
        """Test post batch owner."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'BatchOwner', 'testcase': testcasename})

        # Create batch owner
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/batchowners', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasename)

    def test_get_batchowner(self):
        """Test get batch owner."""
        # Get batch owner
        response = requests.get(self.baseurl + '/v1/batchowners', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_batchowner(self):
        """Test put batch owner."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'BatchOwner', 'testcase': testcasename})

        # Create batch owner
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/batchowners', headers=self.headers, data=payload)
        recordid = response.json()['id']

        testcasenameupdated = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'BatchOwner', 'testcase': testcasenameupdated})

        # Update batch owner
        payload = {}
        payload['id'] = int(recordid)
        payload['name'] = testcasenameupdated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.baseurl + '/v1/batchowners', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasenameupdated)

    def test_delete_batchowner(self):
        """Test delete batch owner."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'BatchOwner', 'testcase': testcasename})

        # Create batch owner
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/batchowners', headers=self.headers, data=payload)

        # Delete batch owner
        response = requests.delete(self.baseurl + '/v1/batchowners', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_post_datasource(self):
        """Test post data source."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'DataSource', 'testcase': testcasename})

        # Create data source
        payload = {}
        payload['name'] = testcasename
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = testcasename
        payload['login'] = testcasename
        payload['password'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/datasources', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasename)

    def test_get_datasource(self):
        """Test get data source."""
        # Get data source
        response = requests.get(self.baseurl + '/v1/datasources', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_datasource(self):
        """Test put data source."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'DataSource', 'testcase': testcasename})

        # Create data source
        payload = {}
        payload['name'] = testcasename
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = testcasename
        payload['login'] = testcasename
        payload['password'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/datasources', headers=self.headers, data=payload)
        recordid = response.json()['id']

        testcasenameupdated = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'DataSource', 'testcase': testcasenameupdated})

        # Update data source
        payload = {}
        payload['id'] = int(recordid)
        payload['name'] = testcasenameupdated
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = testcasenameupdated
        payload['login'] = testcasenameupdated
        payload['password'] = testcasenameupdated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.baseurl + '/v1/datasources', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasenameupdated)

    def test_delete_datasource(self):
        """Test delete data source."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'DataSource', 'testcase': testcasename})

        # Create data source
        payload = {}
        payload['name'] = testcasename
        payload['dataSourceTypeId'] = 1
        payload['connectionString'] = testcasename
        payload['login'] = testcasename
        payload['password'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/datasources', headers=self.headers, data=payload)

        # Delete data source
        response = requests.delete(self.baseurl + '/v1/datasources', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_post_datasourcetype(self):
        """Test post data source type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'DataSourceType', 'testcase': testcasename})

        # Create data source type
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/datasourcetypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasename)

    def test_get_datasourcetype(self):
        """Test get data source type."""
        # Get data source type
        response = requests.get(self.baseurl + '/v1/datasourcetypes', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_datasourcetype(self):
        """Test put data source type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'DataSourceType', 'testcase': testcasename})

        # Create data source type
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/datasourcetypes', headers=self.headers, data=payload)
        recordid = response.json()['id']

        testcasenameupdated = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'DataSourceType', 'testcase': testcasenameupdated})

        # Update data source type
        payload = {}
        payload['id'] = int(recordid)
        payload['name'] = testcasenameupdated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.baseurl + '/v1/datasourcetypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasenameupdated)

    def test_delete_datasourcetype(self):
        """Test delete data source type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'DataSourceType', 'testcase': testcasename})

        # Create data source type
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/datasourcetypes', headers=self.headers, data=payload)

        # Delete data source type
        response = requests.delete(self.baseurl + '/v1/datasourcetypes', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_post_eventtype(self):
        """Test post event type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'EventType', 'testcase': testcasename})

        # Create event type
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/eventtypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasename)

    def test_get_eventtype(self):
        """Test get event type."""
        # Get event type
        response = requests.get(self.baseurl + '/v1/eventtypes', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_eventtype(self):
        """Test put event type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'EventType', 'testcase': testcasename})

        # Create event type
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/eventtypes', headers=self.headers, data=payload)
        recordid = response.json()['id']

        testcasenameupdated = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'EventType', 'testcase': testcasenameupdated})

        # Update event type
        payload = {}
        payload['id'] = int(recordid)
        payload['name'] = testcasenameupdated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.baseurl + '/v1/eventtypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasenameupdated)

    def test_delete_eventtype(self):
        """Test delete event type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'EventType', 'testcase': testcasename})

        # Create event type
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/eventtypes', headers=self.headers, data=payload)

        # Delete event type
        response = requests.delete(self.baseurl + '/v1/eventtypes', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_post_indicatortype(self):
        """Test post indicator type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'IndicatorType', 'testcase': testcasename})

        # Create indicator type
        payload = {}
        payload['name'] = testcasename
        payload['module'] = testcasename
        payload['function'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/indicatortypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasename)

    def test_get_indicatortype(self):
        """Test get indicator type."""
        # Get indicator type
        response = requests.get(self.baseurl + '/v1/indicatortypes', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_indicatortype(self):
        """Test put indicator type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'IndicatorType', 'testcase': testcasename})

        # Create indicator type
        payload = {}
        payload['name'] = testcasename
        payload['module'] = testcasename
        payload['function'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/indicatortypes', headers=self.headers, data=payload)
        recordid = response.json()['id']

        testcasenameupdated = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'IndicatorType', 'testcase': testcasenameupdated})

        # Update indicator type
        payload = {}
        payload['id'] = int(recordid)
        payload['name'] = testcasenameupdated
        payload['module'] = testcasenameupdated
        payload['function'] = testcasenameupdated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.baseurl + '/v1/indicatortypes', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasenameupdated)

    def test_delete_indicatortype(self):
        """Test delete indicator type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'IndicatorType', 'testcase': testcasename})

        # Create indicator type
        payload = {}
        payload['name'] = testcasename
        payload['module'] = testcasename
        payload['function'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/indicatortypes', headers=self.headers, data=payload)

        # Delete indicator type
        response = requests.delete(self.baseurl + '/v1/indicatortypes', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_post_status(self):
        """Test post event type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'Status', 'testcase': testcasename})

        # Create event type
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/status', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasename)

    def test_get_status(self):
        """Test get event type."""
        # Get event type
        response = requests.get(self.baseurl + '/v1/status', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_put_status(self):
        """Test put event type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'Status', 'testcase': testcasename})

        # Create event type
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/status', headers=self.headers, data=payload)
        recordid = response.json()['id']

        testcasenameupdated = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'Status', 'testcase': testcasenameupdated})

        # Update event type
        payload = {}
        payload['id'] = int(recordid)
        payload['name'] = testcasenameupdated
        payload = str(payload).replace("'", '"')
        response = requests.put(self.baseurl + '/v1/status', headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], testcasenameupdated)

    def test_delete_status(self):
        """Test delete event type."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append({'class': 'Status', 'testcase': testcasename})

        # Create event type
        payload = {}
        payload['name'] = testcasename
        payload = str(payload).replace("'", '"')
        response = requests.post(self.baseurl + '/v1/status', headers=self.headers, data=payload)

        # Delete event type
        response = requests.delete(self.baseurl + '/v1/status', headers=self.headers, data=payload)

        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for testcase in self.testcaselist:
            with database.DbOperation(testcase['class']) as op:
                op.delete(name=testcase['testcase'])

if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApiModule)
    unittest.TextTestRunner(verbosity=2).run(suite)
