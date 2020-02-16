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

        connection_string = 'driver={PostgreSQL Unicode};server=db;port=5432;database=mobydq;uid=postgres;pwd=change_me;'  # Should be moved to config file
        connection = pyodbc.connect(connection_string)
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setencoding(encoding='utf-8')
        return connection

    def rollback(self):
        """Rollback uncommitted database transactions."""

        self.connection.execute('ROLLBACK;')
        return True

    def create_data_source(self, test_case_name: str):
        """Create a data source in the database and return its id and password."""

        insert_data_source_query = f'''INSERT INTO base.data_source (name, connection_string, data_source_type_id) VALUES ('{test_case_name}', 'Test connection string', 1) RETURNING id, password;'''
        cursor = self.connection.execute(insert_data_source_query)
        row = cursor.fetchone()

        data_source_id = row[0]
        password = row[1]
        return data_source_id, password

    def create_indicator(self, test_case_name: str, indicator_group_id: int, user_group_id: int):
        """Create an indicator in the database and return its id."""

        insert_indicator_query = f'''INSERT INTO base.indicator (name, flag_active, indicator_type_id, indicator_group_id, user_group_id) VALUES ('{test_case_name}', true, 1, {indicator_group_id}, '{user_group_id}') RETURNING id;'''
        cursor = self.connection.execute(insert_indicator_query)
        indicator_id = cursor.fetchone()[0]
        return indicator_id

    def create_indicator_group(self, test_case_name: str, user_group_id: int):
        """Create an indicator group in the database and return its id."""

        insert_indicator_group_query = f'''INSERT INTO base.indicator_group (name, user_group_id) VALUES ('{test_case_name}', '{user_group_id}') RETURNING id;'''
        cursor = self.connection.execute(insert_indicator_group_query)
        indicator_group_id = cursor.fetchone()[0]
        return indicator_group_id

    def create_user(self, test_case_name: str):
        """Create a user in the database and return its id."""

        insert_user_query = f'''INSERT INTO base.user (email, role) values ('{test_case_name}', 'admin') RETURNING id;'''
        cursor = self.connection.execute(insert_user_query)
        user_id = cursor.fetchone()[0]
        return user_id

    def create_user_group(self, test_case_name: str):
        """Create a user group in the database and return its id."""

        insert_user_group_query = f'''INSERT INTO base.user_group (name) VALUES ('{test_case_name}') RETURNING id;'''
        cursor = self.connection.execute(insert_user_group_query)
        user_group_id = cursor.fetchone()[0]
        return user_group_id

    def create_user_group_membership(self, user_group_id: int, user_id: int):
        """Create a user group user in the database and return its id."""

        insert_user_group_membership_query = f'''INSERT INTO base.user_group_membership (user_group_id, user_id) VALUES ({user_group_id}, {user_id}) RETURNING id;'''
        cursor = self.connection.execute(insert_user_group_membership_query)
        user_group_membership_id = cursor.fetchone()[0]
        return user_group_membership_id

    def delete_user_group(self, user_group_id: int):
        """Delete a user group from the database."""

        delete_user_group_query = f'''DELETE FROM base.user_group WHERE id = {user_group_id};'''
        self.connection.execute(delete_user_group_query)
        return True

    def delete_user_group_membership(self, user_group_id: int):
        """Delete a user group membership from the database."""

        delete_user_group_membership_query = f'''DELETE FROM base.user_group_membership WHERE user_group_id = {user_group_id};'''
        self.connection.execute(delete_user_group_membership_query)
        return True

    def update_user(self, user_id: int):
        """Update a user in the database and return its updated_by_id and updated_date."""

        update_user_query = f'''UPDATE base.user SET role = 'advanced' WHERE id = {user_id} RETURNING updated_by_id, updated_date, created_date;'''
        cursor = self.connection.execute(update_user_query)
        row = cursor.fetchone()

        updated_by_id = row[0]
        updated_date = row[1]
        created_date = row[2]
        return updated_by_id, updated_date, created_date

    def update_data_source(self, data_source_id: int):
        """Update a data source in the database and return its password."""

        update_data_source_query = f'''UPDATE base.data_source SET password = '0000' WHERE id = {data_source_id} RETURNING password;'''
        cursor = self.connection.execute(update_data_source_query)
        password = cursor.fetchone()[0]
        return password

    def test_function_duplicate_indicator(self):
        """Unit tests for custom function duplicate_indicator."""

        # Insert user group
        test_case_name = get_test_case_name()
        user_group_id = self.create_user_group(test_case_name)

        # Insert indicator group
        indicator_group_id = self.create_indicator_group(test_case_name, user_group_id)

        # Insert indicator
        indicator_id = self.create_indicator(test_case_name, indicator_group_id, user_group_id)

        # Insert test parameter
        insert_parameter_query = f'''INSERT INTO base.parameter (value, indicator_id, parameter_type_id, user_group_id) VALUES ('{test_case_name}', {indicator_id}, 1, {user_group_id});'''
        self.connection.execute(insert_parameter_query)

        # Call test duplicate indicator function
        new_test_case_name = get_test_case_name()
        call_test_duplicate_indicator_query = f'''SELECT base.duplicate_indicator({indicator_id}, '{new_test_case_name}');'''
        self.connection.execute(call_test_duplicate_indicator_query)

        # Get new indicator and parameter
        select_new_indicator_query = f'''SELECT a.name, b.value FROM base.indicator a INNER JOIN base.parameter b ON a.id = b.indicator_id WHERE a.name = '{new_test_case_name}';'''
        cursor = self.connection.execute(select_new_indicator_query)
        row = cursor.fetchone()

        # Assert duplicated indicator name and parameter value
        indiator_name = row[0]
        parameter_value = row[1]
        self.assertEqual(indiator_name, new_test_case_name)
        self.assertEqual(parameter_value, test_case_name)

        # Rollback uncommitted data
        self.rollback()

    def test_function_execute_batch(self):
        """Unit tests for custom function execute_batch."""

        # Insert user group
        test_case_name = get_test_case_name()
        user_group_id = self.create_user_group(test_case_name)

        # Insert indicator group
        indicator_group_id = self.create_indicator_group(test_case_name, user_group_id)

        # Insert indicator
        self.create_indicator(test_case_name, indicator_group_id, user_group_id)

        # Call execute batch function
        call_execute_batch_query = f'''SELECT base.execute_batch({indicator_group_id});'''
        self.connection.execute(call_execute_batch_query)

        # Get batch and indicator session
        select_batch_query = f'''SELECT A.status, B.status FROM base.batch A INNER JOIN base.session B ON A.id = B.batch_id WHERE A.indicator_group_id = {indicator_group_id};'''
        cursor = self.connection.execute(select_batch_query)
        row = cursor.fetchone()

        # Assert batch and session status are Pending
        batch_status = row[0]
        session_status = row[1]
        self.assertEqual(batch_status, 'Pending')
        self.assertEqual(session_status, 'Pending')

        # Rollback uncommitted data
        self.rollback()

    def test_function_get_current_user_id(self):
        """Unit tests for custom function get_current_user_id."""

        # Insert user
        test_case_name = get_test_case_name()
        user_id = self.create_user(test_case_name)
        user = f'user_{user_id}'

        # Change role
        set_role_query = f'''SET ROLE {user};'''
        self.connection.execute(set_role_query)

        # Get current user Id based on current role
        select_query = f'''SELECT base.get_current_user_id();'''
        cursor = self.connection.execute(select_query)
        current_user_id = cursor.fetchone()[0]

        # Assert user Id is equal to Id extracted from role
        self.assertEqual(user_id, current_user_id)

        # Reverse current role to postgres
        set_role_query = f'''SET ROLE postgres;'''
        self.connection.execute(set_role_query)

        # Rollback uncommitted data
        self.rollback()

    def test_function_test_data_source(self):
        """Unit tests for custom function test_data_source."""

        # Insert data source
        test_case_name = get_test_case_name()
        data = self.create_data_source(test_case_name)
        data_source_id = data[0]

        # Call test data source function
        call_test_data_source_query = f'''SELECT base.test_data_source({data_source_id});'''
        self.connection.execute(call_test_data_source_query)

        # Get data source connectivity status
        select_data_source_query = f'''SELECT connectivity_status FROM base.data_source WHERE id = '{data_source_id}';'''
        cursor = self.connection.execute(select_data_source_query)
        connectivity_status = cursor.fetchone()[0]

        # Assert connectivity status is Pending
        self.assertEqual(connectivity_status, 'Pending')

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_create_user(self):
        """Unit tests for trigger function create_user."""

        # Insert user
        test_case_name = get_test_case_name()
        user_id = self.create_user(test_case_name)
        user = f'user_{user_id}'

        # Get user and admin role
        select_user_role_query = f'''SELECT a.rolname, c.rolname FROM pg_catalog.pg_roles a INNER JOIN pg_catalog.pg_auth_members b ON a.oid = b.member INNER JOIN pg_catalog.pg_roles c ON b.roleid = c.oid AND c.rolname = 'admin' WHERE a.rolname = '{user}';'''
        cursor = self.connection.execute(select_user_role_query)
        row = cursor.fetchone()

        # Assert user was created and admin role granted
        self.assertEqual(row[0], user)
        self.assertEqual(row[1], 'admin')

        # Get user and default user group
        select_user_role_query = f'''SELECT a.rolname, c.rolname FROM pg_catalog.pg_roles a INNER JOIN pg_catalog.pg_auth_members b ON a.oid = b.member INNER JOIN pg_catalog.pg_roles c ON b.roleid = c.oid AND c.rolname = 'user_group_1' WHERE a.rolname = '{user}';'''
        cursor = self.connection.execute(select_user_role_query)
        row = cursor.fetchone()

        # Assert user was created and user group granted
        self.assertEqual(row[0], user)
        self.assertEqual(row[1], 'user_group_1')

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_create_user_group(self):
        """Unit tests for trigger function create_user_group."""

        # Insert user group
        test_case_name = get_test_case_name()
        user_group_id = self.create_user_group(test_case_name)
        user_group = f'user_group_{user_group_id}'

        # Get user group role
        select_user_role_query = f'''SELECT a.rolname AS user_group FROM pg_catalog.pg_roles a WHERE a.rolname = '{user_group}';'''
        cursor = self.connection.execute(select_user_role_query)
        row = cursor.fetchone()

        # Assert user group role was created
        self.assertEqual(row[0], user_group)

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_data_source_insert_password(self):
        """Unit tests for trigger function data_source_insert_password."""

        # Insert data source
        test_case_name = get_test_case_name()
        data = self.create_data_source(test_case_name)
        password = data[1]

        # Assert password is encrypted
        self.assertNotEqual(password, '1234')

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_data_source_update_password(self):
        """Unit tests for trigger function data_source_update_password."""

        # Insert data source
        test_case_name = get_test_case_name()
        data = self.create_data_source(test_case_name)
        data_source_id = data[0]
        password = data[1]

        # Update data source
        updated_password = self.update_data_source(data_source_id)

        # Assert password is encrypted
        self.assertNotEqual(updated_password, '0000')
        self.assertNotEqual(password, updated_password)

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_delete_children(self):
        """Unit tests for trigger function delete_children."""

        # Insert user
        test_case_name = get_test_case_name()
        user_id = self.create_user(test_case_name)

        # Insert user group
        user_group_id = self.create_user_group(test_case_name)

        # Insert user group membership
        user_group_membership_id = self.create_user_group_membership(user_group_id, user_id)

        # Delete user group
        self.delete_user_group(user_group_id)

        # Get user group membership
        select_user_group_membership_query = f'''SELECT id FROM base.user_group_membership WHERE id = '{user_group_membership_id}';'''
        cursor = self.connection.execute(select_user_group_membership_query)
        row = cursor.fetchone()

        # Assert user group membership has been deleted
        self.assertTrue(row is None)

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_delete_user_group(self):
        """Unit tests for trigger function delete_user_group."""

        # Insert user group
        test_case_name = get_test_case_name()
        user_group_id = self.create_user_group(test_case_name)
        user_group = f'user_group_{user_group_id}'

        # Delete user group
        self.delete_user_group(user_group_id)

        # Get user group role
        select_user_role_query = f'''SELECT a.rolname AS user_group FROM pg_catalog.pg_roles a WHERE a.rolname = '{user_group}';'''
        cursor = self.connection.execute(select_user_role_query)
        row = cursor.fetchone()

        # Assert user group role has been deleted
        self.assertTrue(row is None)

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_grant_user_group(self):
        """Unit tests for trigger function grant_user_group."""

        # Insert user
        test_case_name = get_test_case_name()
        user_id = self.create_user(test_case_name)
        user = f'user_{user_id}'

        # Insert user group
        user_group_id = self.create_user_group(test_case_name)
        user_group = f'user_group_{user_group_id}'

        # Insert user group user
        self.create_user_group_membership(user_group_id, user_id)

        # Get user and user group roles
        select_user_group_membership_query = f'''SELECT a.rolname, c.rolname FROM pg_catalog.pg_roles a INNER JOIN pg_catalog.pg_auth_members b ON a.oid = b.member INNER JOIN pg_catalog.pg_roles c ON b.roleid = c.oid WHERE a.rolname = '{user}' AND c.rolname = '{user_group}';'''
        cursor = self.connection.execute(select_user_group_membership_query)
        row = cursor.fetchone()

        # Assert user was created and user group role granted
        self.assertEqual(row[0], user)
        self.assertEqual(row[1], user_group)

        # Rollback uncommitted data
        self.rollback()

    def test_kill_execute_batch(self):
        """Unit tests for custom function kill_execute_batch."""

        # Insert user group
        test_case_name = get_test_case_name()
        user_group_id = self.create_user_group(test_case_name)

        # Insert indicator group
        indicator_group_id = self.create_indicator_group(test_case_name, user_group_id)

        # Insert indicator
        self.create_indicator(test_case_name, indicator_group_id, user_group_id)

        # Call execute batch function
        call_execute_batch_query = f'''SELECT base.execute_batch({indicator_group_id});'''
        self.connection.execute(call_execute_batch_query)

        # Get batch
        select_batch_query = f'''SELECT A.id FROM base.batch A WHERE A.indicator_group_id = {indicator_group_id};'''
        cursor = self.connection.execute(select_batch_query)
        row = cursor.fetchone()
        batch_id = row[0]

        # Call kill execute batch function
        call_kill_execute_batch_query = f'''SELECT base.kill_execute_batch({batch_id});'''
        self.connection.execute(call_kill_execute_batch_query)

        # Get batch and session with updated status
        select_batch_query = f'''SELECT A.status, B.status FROM base.batch A INNER JOIN base.session B ON A.id = B.batch_id WHERE A.id = {batch_id};'''
        cursor = self.connection.execute(select_batch_query)
        row = cursor.fetchone()

        # Assert batch and session status are Pending
        batch_status = row[0]
        session_status = row[1]
        self.assertEqual(batch_status, 'Killed')
        self.assertEqual(session_status, 'Killed')

        # Rollback uncommitted data
        self.rollback()

    def test_kill_test_data_source(self):
        """Unit tests for custom function kill_test_data_source."""

        # Insert data source
        test_case_name = get_test_case_name()
        data = self.create_data_source(test_case_name)
        data_source_id = data[0]

        # Call test data source function
        call_test_data_source_query = f'''SELECT base.test_data_source({data_source_id});'''
        self.connection.execute(call_test_data_source_query)

        # Call kill test data source function
        call_kill_test_data_source_query = f'''SELECT base.kill_test_data_source({data_source_id});'''
        self.connection.execute(call_kill_test_data_source_query)

        # Get data source connectivity status
        select_data_source_status_query = f'''SELECT A.connectivity_status FROM base.data_source A WHERE A.id = {data_source_id};'''
        cursor = self.connection.execute(select_data_source_status_query)
        row = cursor.fetchone()

        # Assert batch and session status are Pending
        data_source_status = row[0]
        self.assertEqual(data_source_status, 'Killed')

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_revoke_user_group(self):
        """Unit tests for trigger function revoke_user_group."""

        # Insert user
        test_case_name = get_test_case_name()
        user_id = self.create_user(test_case_name)
        user = f'user_{user_id}'

        # Insert user group
        user_group_id = self.create_user_group(test_case_name)
        user_group = f'user_group_{user_group_id}'

        # Insert user group user
        user_group_membership_id = self.create_user_group_membership(user_group_id, user_id)

        # Delete user group user
        insert_user_group_membership_query = f'''DELETE FROM base.user_group_membership WHERE id = {user_group_membership_id};'''
        self.connection.execute(insert_user_group_membership_query)

        # Get user and user group
        select_user_group_membership_query = f'''SELECT a.rolname, c.rolname FROM pg_catalog.pg_roles a INNER JOIN pg_catalog.pg_auth_members b ON a.oid = b.member INNER JOIN pg_catalog.pg_roles c ON b.roleid = c.oid WHERE a.rolname = '{user}' AND c.rolname = '{user_group}';'''
        cursor = self.connection.execute(select_user_group_membership_query)
        row = cursor.fetchone()

        # Assert user group role has been revoked
        self.assertTrue(row is None)

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_update_updated_by_id(self):
        """Unit tests for trigger function update_updated_by_id."""

        # Insert user
        test_case_name = get_test_case_name()
        user_id = self.create_user(test_case_name)
        user = f'user_{user_id}'

        # Change current role to new user
        set_role_query = f'''SET ROLE {user};'''
        self.connection.execute(set_role_query)

        # Update user
        data = self.update_user(user_id)
        updated_by_id = data[0]

        # Assert user Id is equal updated by Id
        self.assertEqual(user_id, updated_by_id)

        # Reverse current role to postgres
        set_role_query = f'''SET ROLE postgres;'''
        self.connection.execute(set_role_query)

        # Rollback uncommitted data
        self.rollback()

    def test_trigger_update_updated_date(self):
        """Unit tests for trigger function update_updated_date."""

        # Insert user
        test_case_name = get_test_case_name()
        user_id = self.create_user(test_case_name)

        # Commit is necessary here for the test case to pass
        # It ensure updated_date will be greater than created_date
        self.connection.commit()

        # Update user
        data = self.update_user(user_id)
        updated_date = data[1]
        created_date = data[2]

        # Assert created_date is older than updated_date
        self.assertLess(created_date, updated_date)

        # Delete committed data
        delete_user_group_membership_query = f'''DELETE FROM base.user_group_membership WHERE user_id = {user_id};'''
        self.connection.execute(delete_user_group_membership_query)

        delete_user_query = f'''DELETE FROM base.user WHERE id = {user_id};'''
        self.connection.execute(delete_user_query)
        self.connection.commit()

    def test_trigger_update_user_permission(self):
        """Unit tests for trigger function update_user_permission."""

        # Insert user
        test_case_name = get_test_case_name()
        user_id = self.create_user(test_case_name)
        user = f'user_{user_id}'

        # Update user role to advanced
        self.update_user(user_id)

        # Get user and role
        select_user_role_query = f'''SELECT a.rolname AS user, c.rolname AS role FROM pg_catalog.pg_roles a INNER JOIN pg_catalog.pg_auth_members b ON a.oid = b.member INNER JOIN pg_catalog.pg_roles c ON b.roleid = c.oid AND c.rolname = 'advanced' WHERE a.rolname = '{user}';'''
        cursor = self.connection.execute(select_user_role_query)
        row = cursor.fetchone()

        # Assert user was created and advanced role granted
        self.assertEqual(row[0], user)
        self.assertEqual(row[1], 'advanced')

        # Rollback uncommitted data
        self.rollback()

    @classmethod
    def tearDownClass(cls):
        """Execute this at the end of the tests."""
        cls.connection.close()


if __name__ == '__main__':
    unittest.main()
