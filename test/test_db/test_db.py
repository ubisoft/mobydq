"""Unit tests for database components."""
import unittest
import pyodbc
from shared.utils import get_test_case_name


class TestDb(unittest.TestCase):
    """Unit tests for database components."""

    @classmethod
    def setUpClass(cls):
        """Execute this before the tests."""
        cls.connection = TestDb.get_connection()

    @staticmethod
    def get_connection():
        """Return connection to mobydq database."""

        connection_string = 'driver={PostgreSQL Unicode};server=db;port=5432;database=mobydq;uid=postgres;pwd=password;'  # Should be moved to config file
        connection = pyodbc.connect(connection_string)
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setencoding(encoding='utf-8')
        return connection

    def test_trigger_update_updated_date(self):
        """Unit tests for trigger update_updated_date."""

        # Insert test record
        test_case_name = get_test_case_name()
        insert_query = f'INSERT INTO base.data_source_type (name) VALUES (\'{test_case_name}\');'
        self.connection.execute(insert_query)
        self.connection.commit()

        # Update test record
        test_case_name_updated = get_test_case_name()
        update_query = f'UPDATE base.data_source_type SET name = \'{test_case_name_updated}\' WHERE name = \'{test_case_name}\';'
        self.connection.execute(update_query)
        self.connection.commit()

        # Get updated record
        select_query = f'SELECT created_date, updated_date FROM base.data_source_type WHERE name = \'{test_case_name_updated}\';'
        cursor = self.connection.execute(select_query)
        row = cursor.fetchone()

        # Assert created_date < updated_date
        created_date = row[0]
        updated_date = row[1]
        self.assertTrue(created_date < updated_date)

    def test_trigger_delete_children(self):
        """Unit tests for trigger delete_children."""

        # Insert test parent record
        test_case_name = get_test_case_name()
        insert_parent_query = f'INSERT INTO base.data_source_type (name) VALUES (\'{test_case_name}\');'
        self.connection.execute(insert_parent_query)
        self.connection.commit()

        # Get test parent record Id
        select_parent_query = f'SELECT id FROM base.data_source_type WHERE name = \'{test_case_name}\';'
        cursor = self.connection.execute(select_parent_query)
        row = cursor.fetchone()
        data_source_type_id = row[0]

        # Insert test child record
        insert_child_query = f'INSERT INTO base.data_source (name, data_source_type_id, user_group) VALUES (\'{test_case_name}\', \'{data_source_type_id}\', \'test_group\');'
        self.connection.execute(insert_child_query)
        self.connection.commit()

        # Delete test parent record
        delete_parent_query = f'DELETE FROM base.data_source_type WHERE id = {data_source_type_id}'
        self.connection.execute(delete_parent_query)
        self.connection.commit()

        # Gat test child record
        select_child_query = f'SELECT id FROM base.data_source WHERE name = \'{test_case_name}\';'
        cursor = self.connection.execute(select_child_query)
        row = cursor.fetchone()

        # Assert test child record has been deleted
        self.assertTrue(row is None)

    def test_function_execute_batch(self):
        """Unit tests for custom function execute_batch."""

        # Insert test indicator group
        test_case_name = get_test_case_name()
        insert_indicator_group_query = f'INSERT INTO base.indicator_group (name, user_group) VALUES (\'{test_case_name}\', \'test_group\');'
        self.connection.execute(insert_indicator_group_query)
        self.connection.commit()

        # Get test indicator group Id
        select_indicator_group_query = f'SELECT id FROM base.indicator_group WHERE name = \'{test_case_name}\';'
        cursor = self.connection.execute(select_indicator_group_query)
        row = cursor.fetchone()
        indicator_group_id = row[0]

        # Insert test indicator
        insert_indicator_query = f'''INSERT INTO base.indicator (name, flag_active, indicator_type_id, indicator_group_id, user_group)
        VALUES ('{test_case_name}', true, 1, {indicator_group_id}, 'test_group');'''
        self.connection.execute(insert_indicator_query)
        self.connection.commit()

        # Call execute batch function
        call_execute_batch_query = f'SELECT base.execute_batch({indicator_group_id});'
        self.connection.execute(call_execute_batch_query)

        # Get batch and indicator session
        select_batch_query = f'''SELECT B.status, C.status FROM base.indicator_group A
        INNER JOIN base.batch B ON A.id = B.indicator_group_id
        INNER JOIN base.session C ON B.id = C.batch_id
        WHERE A.name = '{test_case_name}';'''
        cursor = self.connection.execute(select_batch_query)
        row = cursor.fetchone()

        # Assert batch and session status are Pending
        batch_status = row[0]
        session_status = row[1]
        self.assertEqual(batch_status, 'Pending')
        self.assertEqual(session_status, 'Pending')

    def test_function_test_data_source(self):
        """Unit tests for custom function test_data_source."""

        # Insert test data source
        test_case_name = get_test_case_name()
        insert_data_source_query = f'INSERT INTO base.data_source (name, data_source_type_id, user_group) VALUES (\'{test_case_name}\', 1, \'test_group\');'
        self.connection.execute(insert_data_source_query)
        self.connection.commit()

        # Get test data source Id
        select_data_source_query = f'SELECT id FROM base.data_source WHERE name = \'{test_case_name}\';'
        cursor = self.connection.execute(select_data_source_query)
        row = cursor.fetchone()
        data_source_id = row[0]

        # Call test data source function
        call_test_data_source_query = f'SELECT base.test_data_source({data_source_id});'
        self.connection.execute(call_test_data_source_query)

        # Get data source connectivity status
        select_data_source_query = f'SELECT connectivity_status FROM base.data_source WHERE name = \'{test_case_name}\';'
        cursor = self.connection.execute(select_data_source_query)
        row = cursor.fetchone()

        # Assert connectivity status is Pending
        connectivity_status = row[0]
        self.assertEqual(connectivity_status, 'Pending')

    def test_function_duplicate_indicator(self):
        """Unit tests for custom function duplicate_indicator."""

        # Insert test indicator group
        test_case_name = get_test_case_name()
        insert_indicator_group_query = f'INSERT INTO base.indicator_group (name, user_group) VALUES (\'{test_case_name}\', \'test_group\');'
        self.connection.execute(insert_indicator_group_query)
        self.connection.commit()

        # Get test indicator group Id
        select_indicator_group_query = f'SELECT id FROM base.indicator_group WHERE name = \'{test_case_name}\';'
        cursor = self.connection.execute(select_indicator_group_query)
        row = cursor.fetchone()
        indicator_group_id = row[0]

        # Insert test indicator
        insert_indicator_query = f'''INSERT INTO base.indicator (name, flag_active, indicator_type_id, indicator_group_id, user_group)
        VALUES ('{test_case_name}', true, 1, {indicator_group_id}, 'test_group');'''
        self.connection.execute(insert_indicator_query)
        self.connection.commit()

        # Get test indicator Id
        select_indicator_query = f'SELECT id FROM base.indicator WHERE name = \'{test_case_name}\';'
        cursor = self.connection.execute(select_indicator_query)
        row = cursor.fetchone()
        indicator_id = row[0]

        # Insert test parameter
        insert_parameter_query = f'INSERT INTO base.parameter (value, indicator_id, parameter_type_id, user_group) VALUES (\'{test_case_name}\', {indicator_id}, 1, \'test_group\');'
        self.connection.execute(insert_parameter_query)
        self.connection.commit()

        # Call test duplicate indicator function
        new_test_case_name = get_test_case_name()
        call_test_duplicate_indicator_query = f'SELECT base.duplicate_indicator({indicator_id}, \'{new_test_case_name}\');'
        self.connection.execute(call_test_duplicate_indicator_query)

        # Get new indicator and parameter
        select_new_indicator_query = f'''SELECT a.name, b.value FROM base.indicator a
        INNER JOIN base.parameter b ON a.id=b.indicator_id
        WHERE name = '{new_test_case_name}';'''
        cursor = self.connection.execute(select_new_indicator_query)
        row = cursor.fetchone()

        # Assert duplicated indicator name and parameter value
        name = row[0]
        value = row[0]
        self.assertEqual(name, new_test_case_name)
        self.assertEqual(value, new_test_case_name)

    def test_function_create_new_user_group(self):
        # Insert test create new user group
        test_case_name = get_test_case_name()
        call_test_create_new_user_group_query = f'SELECT base.create_new_user_group(\'{test_case_name}\');'
        self.connection.execute(call_test_create_new_user_group_query)

        # Get new created standard user group role
        select_new_standard_group_role_query = f'''SELECT rolsuper FROM pg_roles
        WHERE rolname = 'user_group_' || '{test_case_name}';'''
        cursor = self.connection.execute(select_new_standard_group_role_query)
        row_user_role = cursor.fetchone()

        # Get new created admin user group role
        select_new_admin_group_role_query = f'''SELECT rolsuper FROM pg_roles
        WHERE rolname = 'user_group_' || '{test_case_name}' || '_admin';'''
        cursor = self.connection.execute(select_new_admin_group_role_query)
        row_admin_role = cursor.fetchone()

        # Get number of new created user group policies
        select_all_user_group_policies_query = f'''SELECT COUNT(*) FROM pg_catalog.pg_policies
        WHERE policyname LIKE 'user_group_' || '{test_case_name}' || '%';'''
        cursor = self.connection.execute(select_all_user_group_policies_query)
        row_number_policies = cursor.fetchone()

        # Get new created indicator_group policy
        select_indicator_group_policy_query = f'''SELECT cmd FROM pg_catalog.pg_policies
        WHERE policyname = 'user_group_' || '{test_case_name}' || '_indicator_group_all';'''
        cursor = self.connection.execute(select_indicator_group_policy_query)
        row_indicator_group_policy = cursor.fetchone()

        # Get new created data_source policy for standard user of user group
        select_data_source_policy_query = f'''SELECT cmd FROM pg_catalog.pg_policies
        WHERE policyname = 'user_group_' || '{test_case_name}' || '_data_source_select';'''
        cursor = self.connection.execute(select_data_source_policy_query)
        row_data_source_policy = cursor.fetchone()

        # Get new created data_source policy for admin user of user group
        select_data_source_policy_admin_query = f'''SELECT cmd FROM pg_catalog.pg_policies
        WHERE policyname LIKE 'user_group_' || '{test_case_name}' || '_admin_data_source_a%';'''
        cursor = self.connection.execute(select_data_source_policy_admin_query)
        row_data_source_policy_admin = cursor.fetchone()

        # Assert roles and policy creation works as expected
        self.assertEqual(row_user_role[0], '0')
        self.assertEqual(row_admin_role[0], '0')
        self.assertEqual(row_number_policies[0], 8)
        self.assertEqual(row_indicator_group_policy[0], 'ALL')
        self.assertEqual(row_data_source_policy[0], 'SELECT')
        self.assertEqual(row_data_source_policy_admin[0], 'ALL')

    def test_function_create_new_user_role(self):
        # Insert test create new user
        test_case_name = get_test_case_name()
        call_test_create_new_user_role_query = f'INSERT INTO base.user (email, oauth_type, access_token, expiry_date) values (\'{test_case_name}\', \'google\', \'1234\', CURRENT_TIMESTAMP) RETURNING id;'
        cursor = self.connection.execute(call_test_create_new_user_role_query)
        id_of_new_role = cursor.fetchone()[0]

        # Get new created user role
        select_new_role_query = f'''SELECT COUNT(*) FROM pg_roles
        WHERE rolname = 'user_' || '{id_of_new_role}';'''
        cursor = self.connection.execute(select_new_role_query)
        row_count_user_role = cursor.fetchone()

        # Assert roles creation works as expected
        self.assertEqual(row_count_user_role[0], 1)

    def test_function_get_all_user_groups(self):
        # Insert test get all user group roles

        # Prepare database, delete all user group roles in the pg_authid table
        delete_user_groups_roles = 'DELETE FROM pg_authid WHERE rolname LIKE \'user_group_%\';'
        self.connection.execute(delete_user_groups_roles)

        # Create new user groups
        create_test_user_group_standard = 'CREATE ROLE user_group_mobydq;'
        self.connection.execute(create_test_user_group_standard)
        create_test_user_group_admin = 'CREATE ROLE user_group_mobydq_admin;'
        self.connection.execute(create_test_user_group_admin)

        # Call tested function to get all user groups
        call_test_get_all_user_groups = 'SELECT base.get_all_user_groups();'
        cursor = self.connection.execute(call_test_get_all_user_groups)
        user_group_list = list(cursor)

        # Assert all created user groups are in the returned list
        user_group_names = [item[0] for item in user_group_list]
        self.assertTrue('user_group_mobydq' in user_group_names)
        self.assertTrue('user_group_mobydq_admin' in user_group_names)

    def test_function_get_all_user_groups_by_user(self):
        # Insert test get all user group roles of user

        # Prepare database, delete test user and test user group role
        delete_user_role = 'DELETE FROM pg_authid WHERE rolname LIKE \'user_mobydq\';'
        self.connection.execute(delete_user_role)
        delete_user_group_role = 'DELETE FROM pg_authid WHERE rolname LIKE \'user_group_mobydq\';'
        self.connection.execute(delete_user_group_role)

        # Create new user and a new user group role, grant user group to user
        create_new_user = 'CREATE ROLE user_mobydq;'
        self.connection.execute(create_new_user)
        create_new_user_group = 'CREATE ROLE user_group_mobydq;'
        self.connection.execute(create_new_user_group)
        grant_user_group_roles_to_user = 'GRANT user_group_mobydq TO user_mobydq;'
        self.connection.execute(grant_user_group_roles_to_user)

        call_test_get_all_user_groups_by_user = 'SELECT base.get_all_user_groups_by_user(\'user_mobydq\');'
        cursor = self.connection.execute(call_test_get_all_user_groups_by_user)
        user_group_list = list(cursor)

        # Assert granted user group roles were selected and are in returned list
        self.assertTrue('user_group_mobydq' in [item[0] for item in user_group_list])

    @classmethod
    def tearDownClass(cls):
        """Execute this at the end of the tests."""
        cls.connection.close()


if __name__ == '__main__':
    unittest.main()
