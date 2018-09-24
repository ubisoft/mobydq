from datetime import datetime
import pyodbc
import time
import unittest


class TestDb(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connection = TestDb.get_connection()

    @staticmethod
    def get_test_case_name():
        """Generate unique name for unit test case."""
        time.sleep(1)
        test_case_name = 'test {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return test_case_name

    @staticmethod
    def get_connection():
        """Return connection to data_quality database."""
        connection_string = 'driver={PostgreSQL Unicode};server=0.0.0.0;port=5432;database=data_quality;uid=postgres;pwd=password;'
        connection = pyodbc.connect(connection_string)
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setencoding(encoding='utf-8')
        return connection

    def test_trigger_update_updated_date(self):
        # Insert test record
        test_case_name = TestDb.get_test_case_name()
        insert_query = "INSERT INTO base.data_source_type (name) VALUES ('{}');".format(test_case_name)
        self.connection.execute(insert_query)
        self.connection.commit()

        # Update test record
        test_case_name_updated = TestDb.get_test_case_name()
        update_query = "UPDATE base.data_source_type SET name = '{}' WHERE name = '{}';".format(test_case_name_updated, test_case_name)
        self.connection.execute(update_query)
        self.connection.commit()

        # Get updated record
        select_query = "SELECT created_date, updated_date FROM base.data_source_type WHERE name = '{}';".format(test_case_name_updated)
        cursor = self.connection.execute(select_query)
        row = cursor.fetchone()

        # Assert created_date < updated_date
        created_date = row[0]
        updated_date = row[1]
        self.assertTrue(created_date < updated_date)

    def test_trigger_delete_children(self):
        # Insert test parent record
        test_case_name = TestDb.get_test_case_name()
        insert_parent_query = "INSERT INTO base.data_source_type (name) VALUES ('{}');".format(test_case_name)
        self.connection.execute(insert_parent_query)
        self.connection.commit()

        # Get test parent record Id
        select_parent_query = "SELECT id FROM base.data_source_type WHERE name = '{}';".format(test_case_name)
        cursor = self.connection.execute(select_parent_query)
        row = cursor.fetchone()
        data_source_type_id = row[0]

        # Insert test child record
        insert_child_query = "INSERT INTO base.data_source (name, data_source_type_id) VALUES ('{}', '{}');""".format(test_case_name, data_source_type_id)
        self.connection.execute(insert_child_query)
        self.connection.commit()

        # Delete test parent record
        delete_parent_query = "DELETE FROM base.data_source_type WHERE id = {}".format(data_source_type_id)
        self.connection.execute(delete_parent_query)
        self.connection.commit()

        # Gat test child record
        select_child_query = "SELECT id FROM base.data_source WHERE name = '{}';".format(test_case_name)
        cursor = self.connection.execute(select_child_query)
        row = cursor.fetchone()

        # Assert test child record has been deleted
        self.assertTrue(row is None)

    def test_function_execute_batch(self):
        # Insert test indicator group
        test_case_name = TestDb.get_test_case_name()
        insert_indicator_group_query = "INSERT INTO base.indicator_group (name) VALUES ('{}');".format(test_case_name)
        self.connection.execute(insert_indicator_group_query)
        self.connection.commit()

        # Get test indicator group Id
        select_indicator_group_query = "SELECT id FROM base.indicator_group WHERE name = '{}';".format(test_case_name)
        cursor = self.connection.execute(select_indicator_group_query)
        row = cursor.fetchone()
        indicator_group_id = row[0]

        # Insert test indicator
        insert_indicator_query = """INSERT INTO base.indicator (name, flag_active, indicator_type_id, indicator_group_id)
        VALUES ('{}', true, 1, {});""".format(test_case_name, indicator_group_id)
        self.connection.execute(insert_indicator_query)
        self.connection.commit()

        # Call execute batch function
        call_execute_batch_query = "SELECT base.execute_batch({});".format(indicator_group_id)
        self.connection.execute(call_execute_batch_query)

        # Get batch and indicator session
        select_batch_query = """SELECT B.status, C.status FROM base.indicator_group A
        INNER JOIN base.batch B ON A.id = B.indicator_group_id
        INNER JOIN base.session C ON B.id = C.batch_id
        WHERE A.name = '{}';""".format(test_case_name)
        cursor = self.connection.execute(select_batch_query)
        row = cursor.fetchone()

        # Assert batch and session status are Pending
        batch_status = row[0]
        session_status = row[1]
        self.assertEqual(batch_status, 'Pending')
        self.assertEqual(session_status, 'Pending')

    def test_function_test_data_source(self):
        # Insert test data source
        test_case_name = TestDb.get_test_case_name()
        insert_data_source_query = "INSERT INTO base.data_source (name, data_source_type_id) VALUES ('{}', 1);".format(test_case_name)
        self.connection.execute(insert_data_source_query)
        self.connection.commit()

        # Get test data source Id
        select_data_source_query = "SELECT id FROM base.data_source WHERE name = '{}';".format(test_case_name)
        cursor = self.connection.execute(select_data_source_query)
        row = cursor.fetchone()
        data_source_id = row[0]

        # Call test data source function
        call_test_data_source_query = "SELECT base.test_data_source({});".format(data_source_id)
        self.connection.execute(call_test_data_source_query)

        # Get data source connectivity status
        select_data_source_query = "SELECT connectivity_status FROM base.data_source WHERE name = '{}';".format(test_case_name)
        cursor = self.connection.execute(select_data_source_query)
        row = cursor.fetchone()

        # Assert connectivity status is Pending
        connectivity_status = row[0]
        self.assertEqual(connectivity_status, 'Pending')

    def test_function_duplicate_indicator(self):
        # Insert test indicator group
        test_case_name = TestDb.get_test_case_name()
        insert_indicator_group_query = "INSERT INTO base.indicator_group (name) VALUES ('{}');".format(test_case_name)
        self.connection.execute(insert_indicator_group_query)
        self.connection.commit()

        # Get test indicator group Id
        select_indicator_group_query = "SELECT id FROM base.indicator_group WHERE name = '{}';".format(test_case_name)
        cursor = self.connection.execute(select_indicator_group_query)
        row = cursor.fetchone()
        indicator_group_id = row[0]

        # Insert test indicator
        insert_indicator_query = """INSERT INTO base.indicator (name, flag_active, indicator_type_id, indicator_group_id)
        VALUES ('{}', true, 1, {});""".format(test_case_name, indicator_group_id)
        self.connection.execute(insert_indicator_query)
        self.connection.commit()

        # Get test indicator Id
        select_indicator_query = "SELECT id FROM base.indicator WHERE name = '{}';".format(test_case_name)
        cursor = self.connection.execute(select_indicator_query)
        row = cursor.fetchone()
        indicator_id = row[0]

        # Insert test parameter
        insert_parameter_query = "INSERT INTO base.parameter (value, indicator_id, parameter_type_id) VALUES ('{}', {}, 1);".format(test_case_name, indicator_id)
        self.connection.execute(insert_parameter_query)
        self.connection.commit()

        # Call test duplicate indicator function
        new_test_case_name = TestDb.get_test_case_name()
        call_test_duplicate_indicator_query = "SELECT base.duplicate_indicator({}, '{}');".format(indicator_id, new_test_case_name)
        self.connection.execute(call_test_duplicate_indicator_query)

        # Get new indicator and parameter
        select_new_indicator_query = """SELECT a.name, b.value FROM base.indicator a
        INNER JOIN base.parameter b ON a.id=b.indicator_id
        WHERE name = '{}';""".format(new_test_case_name)
        cursor = self.connection.execute(select_new_indicator_query)
        row = cursor.fetchone()

        # Assert connectivity status is Pending
        name = row[0]
        value = row[0]
        self.assertEqual(name, new_test_case_name)
        self.assertEqual(value, new_test_case_name)

    @classmethod
    def tearDownClass(self):
        self.connection.close()


if __name__ == '__main__':
    unittest.main()
