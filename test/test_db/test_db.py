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

    def test_function_duplicate_indicator(self):
        """Unit tests for custom function duplicate_indicator."""

        # Insert test indicator group
        test_case_name = get_test_case_name()
        insert_indicator_group_query = f'''INSERT INTO base.indicator_group (name, user_group) VALUES ('{test_case_name}', '{test_case_name}') RETURNING id;'''
        cursor = self.connection.execute(insert_indicator_group_query)
        self.connection.commit()
        indicator_group_id = cursor.fetchone()[0]

        # Insert test indicator
        insert_indicator_query = f'''INSERT INTO base.indicator (name, flag_active, indicator_type_id, indicator_group_id, user_group) VALUES ('{test_case_name}', true, 1, {indicator_group_id}, '{test_case_name}') RETURNING id;'''
        cursor = self.connection.execute(insert_indicator_query)
        self.connection.commit()
        indicator_id = cursor.fetchone()[0]

        # Insert test parameter
        insert_parameter_query = f'''INSERT INTO base.parameter (value, indicator_id, parameter_type_id, user_group) VALUES ('{test_case_name}', {indicator_id}, 1, 'test_group');'''
        self.connection.execute(insert_parameter_query)
        self.connection.commit()

        # Call test duplicate indicator function
        new_test_case_name = get_test_case_name()
        call_test_duplicate_indicator_query = f'''SELECT base.duplicate_indicator({indicator_id}, '{new_test_case_name}');'''
        self.connection.execute(call_test_duplicate_indicator_query)

        # Get new indicator and parameter
        select_new_indicator_query = f'''SELECT a.name, b.value FROM base.indicator a INNER JOIN base.parameter b ON a.id=b.indicator_id WHERE name = '{new_test_case_name}';'''
        cursor = self.connection.execute(select_new_indicator_query)
        row = cursor.fetchone()

        # Assert duplicated indicator name and parameter value
        name = row[0]
        value = row[1]
        self.assertEqual(name, new_test_case_name)
        self.assertEqual(value, test_case_name)

    def test_function_execute_batch(self):
        """Unit tests for custom function execute_batch."""

        # Insert test indicator group
        test_case_name = get_test_case_name()
        insert_indicator_group_query = f'''INSERT INTO base.indicator_group (name, user_group) VALUES ('{test_case_name}', 'test_group') RETURNING id;'''
        cursor = self.connection.execute(insert_indicator_group_query)
        self.connection.commit()
        indicator_group_id = cursor.fetchone()[0]

        # Insert test indicator
        insert_indicator_query = f'''INSERT INTO base.indicator (name, flag_active, indicator_type_id, indicator_group_id, user_group) VALUES ('{test_case_name}', true, 1, {indicator_group_id}, 'test_group');'''
        self.connection.execute(insert_indicator_query)
        self.connection.commit()

        # Call execute batch function
        call_execute_batch_query = f'''SELECT base.execute_batch({indicator_group_id});'''
        self.connection.execute(call_execute_batch_query)

        # Get batch and indicator session
        select_batch_query = f'''SELECT B.status, C.status FROM base.indicator_group A INNER JOIN base.batch B ON A.id = B.indicator_group_id INNER JOIN base.session C ON B.id = C.batch_id WHERE A.name = '{test_case_name}';'''
        cursor = self.connection.execute(select_batch_query)
        row = cursor.fetchone()

        # Assert batch and session status are Pending
        batch_status = row[0]
        session_status = row[1]
        self.assertEqual(batch_status, 'Pending')
        self.assertEqual(session_status, 'Pending')

    def test_function_get_current_user_id(self):
        """Unit tests for custom function get_current_user_id."""

        # Need dedicated database session to change current user role
        session = TestDb.get_connection()

        # Insert user
        test_case_name = get_test_case_name()
        insert_user_query = f'''INSERT INTO base.user (email, oauth_type, access_token, expiry_date) values ('{test_case_name}', 'GOOGLE', '1234', '2999-12-31') RETURNING id;'''
        cursor = session.execute(insert_user_query)
        session.commit()

        # Get user Id and change role
        user_id = cursor.fetchone()[0]
        role = f'user_{user_id}'
        set_role_query = f'''SET ROLE {role};'''
        session.execute(set_role_query)

        # Get current user Id based on current role
        select_query = f'''SELECT base.get_current_user_id();'''
        cursor = session.execute(select_query)
        row = cursor.fetchone()

        # Assert user Id is equal to Id extracted from role
        self.assertEqual(user_id, row[0])
        session.close()

    def test_function_test_data_source(self):
        """Unit tests for custom function test_data_source."""

        # Insert test data source
        test_case_name = get_test_case_name()
        insert_data_source_query = f'''INSERT INTO base.data_source (name, data_source_type_id, user_group) VALUES ('{test_case_name}', 1, 'test_group') RETURNING id;'''
        cursor = self.connection.execute(insert_data_source_query)
        self.connection.commit()
        data_source_id = cursor.fetchone()[0]

        # Call test data source function
        call_test_data_source_query = f'''SELECT base.test_data_source({data_source_id});'''
        self.connection.execute(call_test_data_source_query)

        # Get data source connectivity status
        select_data_source_query = f'''SELECT connectivity_status FROM base.data_source WHERE name = '{test_case_name}';'''
        cursor = self.connection.execute(select_data_source_query)
        connectivity_status = cursor.fetchone()[0]

        # Assert connectivity status is Pending
        self.assertEqual(connectivity_status, 'Pending')

    def test_trigger_create_user(self):
        """Unit tests for trigger function create_user."""

        # Insert user
        test_case_name = get_test_case_name()
        insert_user_query = f'''INSERT INTO base.user (email, oauth_type, access_token, expiry_date) values ('{test_case_name}', 'GOOGLE', '1234', '2999-12-31') RETURNING id;'''
        cursor = self.connection.execute(insert_user_query)
        user_id = cursor.fetchone()[0]
        user = f'user_{user_id}'

        # Get user and role
        select_user_role_query = f'''SELECT a.rolname, c.rolname FROM pg_catalog.pg_roles a INNER JOIN pg_catalog.pg_auth_members b ON a.oid=b.member INNER JOIN pg_catalog.pg_roles c ON b.roleid=c.oid WHERE a.rolname='{user}';'''
        cursor = self.connection.execute(select_user_role_query)
        row = cursor.fetchone()

        # Assert user was created and standard role granted
        self.assertEqual(row[0], user)
        self.assertEqual(row[1], 'standard')

    def test_trigger_create_user_group(self):
        """Unit tests for trigger function create_user_group."""

        # Insert user group
        test_case_name = get_test_case_name()
        insert_user_group_query = f'''INSERT INTO base.user_group (name) VALUES ('{test_case_name}') RETURNING id;'''
        cursor = self.connection.execute(insert_user_group_query)
        self.connection.commit()
        user_group_id = cursor.fetchone()[0]
        user_group = f'user_group_{user_group_id}'

        # Get user group role
        select_user_role_query = f'''SELECT a.rolname AS user_group FROM pg_catalog.pg_roles a WHERE a.rolname='{user_group}';'''
        cursor = self.connection.execute(select_user_role_query)
        row = cursor.fetchone()

        # Assert user group role was created
        self.assertEqual(row[0], user_group)

    def test_trigger_delete_children(self):
        """Unit tests for trigger function delete_children."""

        # Insert parent record
        test_case_name = get_test_case_name()
        insert_parent_query = f'''INSERT INTO base.data_source_type (name) VALUES ('{test_case_name}') RETURNING id;'''
        cursor = self.connection.execute(insert_parent_query)
        self.connection.commit()
        row = cursor.fetchone()
        data_source_type_id = row[0]

        # Insert child record
        insert_child_query = f'''INSERT INTO base.data_source (name, data_source_type_id, user_group) VALUES ('{test_case_name}', '{data_source_type_id}', 'test_group');'''
        self.connection.execute(insert_child_query)
        self.connection.commit()

        # Delete parent record
        delete_parent_query = f'''DELETE FROM base.data_source_type WHERE id = {data_source_type_id}'''
        self.connection.execute(delete_parent_query)
        self.connection.commit()

        # Get child record
        select_child_query = f'''SELECT id FROM base.data_source WHERE name = '{test_case_name}';'''
        cursor = self.connection.execute(select_child_query)
        row = cursor.fetchone()

        # Assert child record has been deleted
        self.assertTrue(row is None)

    def test_trigger_delete_user_group(self):
        """Unit tests for trigger function delete_user_group."""

        # Insert user group
        test_case_name = get_test_case_name()
        insert_user_group_query = f'''INSERT INTO base.user_group (name) VALUES ('{test_case_name}') RETURNING id;'''
        cursor = self.connection.execute(insert_user_group_query)
        self.connection.commit()
        user_group_id = cursor.fetchone()[0]
        user_group = f'user_group_{user_group_id}'

        # Delete user group
        delete_user_group_query = f'''DELETE FROM base.user_group WHERE name = '{test_case_name}';'''
        self.connection.execute(delete_user_group_query)
        self.connection.commit()

        # Get user group role
        select_user_role_query = f'''SELECT a.rolname AS user_group FROM pg_catalog.pg_roles a WHERE a.rolname='{user_group}';'''
        cursor = self.connection.execute(select_user_role_query)
        row = cursor.fetchone()

        # Assert user group role has been deleted
        self.assertTrue(row is None)

    def test_trigger_grant_user_group(self):
        """Unit tests for trigger function grant_user_group."""

        # Insert user
        test_case_name = get_test_case_name()
        insert_user_query = f'''INSERT INTO base.user (email, oauth_type, access_token, expiry_date) values ('{test_case_name}', 'GOOGLE', '1234', '2999-12-31') RETURNING id;'''
        cursor = self.connection.execute(insert_user_query)
        self.connection.commit()
        user_id = cursor.fetchone()[0]
        user = f'user_{user_id}'

        # Insert user group
        new_test_case_name = get_test_case_name()
        insert_user_group_query = f'''INSERT INTO base.user_group (name) VALUES ('{new_test_case_name}') RETURNING id;'''
        cursor = self.connection.execute(insert_user_group_query)
        self.connection.commit()
        user_group_id = cursor.fetchone()[0]
        user_group = f'user_group_{user_group_id}'

        # Insert user group user
        insert_user_group_user_query = f'''INSERT INTO base.user_group_user (user_group_id, user_id) VALUES ({user_group_id}, {user_id});'''
        self.connection.execute(insert_user_group_user_query)
        self.connection.commit()

        # Get user and user group
        select_user_group_user_query = f'''SELECT a.rolname, c.rolname FROM pg_catalog.pg_roles a INNER JOIN pg_catalog.pg_auth_members b ON a.oid = b.member INNER JOIN pg_catalog.pg_roles c ON b.roleid = c.oid WHERE a.rolname = '{user}' AND c.rolname = '{user_group}';'''
        cursor = self.connection.execute(select_user_group_user_query)
        row = cursor.fetchone()

        # Assert user was created and user group role granted
        self.assertEqual(row[0], user)
        self.assertEqual(row[1], user_group)

    def test_trigger_revoke_user_group(self):
        """Unit tests for trigger function revoke_user_group."""

        # Insert user
        test_case_name = get_test_case_name()
        insert_user_query = f'''INSERT INTO base.user (email, oauth_type, access_token, expiry_date) values ('{test_case_name}', 'GOOGLE', '1234', '2999-12-31') RETURNING id;'''
        cursor = self.connection.execute(insert_user_query)
        self.connection.commit()
        user_id = cursor.fetchone()[0]
        user = f'user_{user_id}'

        # Insert user group
        new_test_case_name = get_test_case_name()
        insert_user_group_query = f'''INSERT INTO base.user_group (name) VALUES ('{new_test_case_name}') RETURNING id;'''
        cursor = self.connection.execute(insert_user_group_query)
        self.connection.commit()
        user_group_id = cursor.fetchone()[0]
        user_group = f'user_group_{user_group_id}'

        # Insert user group user
        insert_user_group_user_query = f'''INSERT INTO base.user_group_user (user_group_id, user_id) VALUES ({user_group_id}, {user_id}) RETURNING id;'''
        cursor = self.connection.execute(insert_user_group_user_query)
        self.connection.commit()
        user_group_user_id = cursor.fetchone()[0]

        # Delete user group user
        insert_user_group_user_query = f'''DELETE FROM base.user_group_user WHERE id = {user_group_user_id};'''
        self.connection.execute(insert_user_group_user_query)
        self.connection.commit()

        # Get user and user group
        select_user_group_user_query = f'''SELECT a.rolname, c.rolname FROM pg_catalog.pg_roles a INNER JOIN pg_catalog.pg_auth_members b ON a.oid = b.member INNER JOIN pg_catalog.pg_roles c ON b.roleid = c.oid WHERE a.rolname = '{user}' AND c.rolname = '{user_group}';'''
        cursor = self.connection.execute(select_user_group_user_query)
        row = cursor.fetchone()

        # Assert user group role has been revoked
        self.assertTrue(row is None)

    def test_trigger_update_updated_by_id(self):
        """Unit tests for trigger function update_updated_by_id."""

        # Need dedicated database session to change current user role
        session = TestDb.get_connection()

        # Insert test record
        test_case_name = get_test_case_name()
        insert_query = f'''INSERT INTO base.data_source_type (name) VALUES ('{test_case_name}');'''
        session.execute(insert_query)
        session.commit()

        # Insert user
        insert_user_query = f'''INSERT INTO base.user (email, oauth_type, access_token, expiry_date, flag_admin) values ('{test_case_name}', 'GOOGLE', '1234', '2999-12-31', true) RETURNING id;'''
        cursor = session.execute(insert_user_query)
        session.commit()

        # Change role
        user_id = cursor.fetchone()[0]
        role = f'user_{user_id}'
        set_role_query = f'''SET ROLE {role};'''
        session.execute(set_role_query)

        # Update test record
        test_case_name_updated = get_test_case_name()
        update_query = f'''UPDATE base.data_source_type SET name = '{test_case_name_updated}' WHERE name = '{test_case_name}' RETURNING updated_by_id;'''
        cursor = session.execute(update_query)
        session.commit()
        row = cursor.fetchone()

        # Assert user Id is equal updated by Id
        self.assertEqual(user_id, row[0])

    def test_trigger_update_updated_date(self):
        """Unit tests for trigger function update_updated_date."""

        # Insert test record
        test_case_name = get_test_case_name()
        insert_query = f'''INSERT INTO base.data_source_type (name) VALUES ('{test_case_name}');'''
        self.connection.execute(insert_query)
        self.connection.commit()

        # Update test record
        test_case_name_updated = get_test_case_name()
        update_query = f'''UPDATE base.data_source_type SET name = '{test_case_name_updated}' WHERE name = '{test_case_name}' RETURNING created_date, updated_date;'''
        cursor = self.connection.execute(update_query)
        self.connection.commit()
        row = cursor.fetchone()

        # Assert created_date < updated_date
        created_date = row[0]
        updated_date = row[1]
        self.assertLess(created_date, updated_date)

    def test_trigger_update_user_permission(self):
        """Unit tests for trigger function update_user_permission."""

        # Insert user
        test_case_name = get_test_case_name()
        insert_user_query = f'''INSERT INTO base.user (email, oauth_type, access_token, expiry_date) values ('{test_case_name}', 'GOOGLE', '1234', '2999-12-31') RETURNING id;'''
        cursor = self.connection.execute(insert_user_query)
        self.connection.commit()
        user_id = cursor.fetchone()[0]
        user = f'user_{user_id}'

        # Update user role to admin
        update_user_query = f'UPDATE base.user SET flag_admin = true WHERE id={user_id};'
        self.connection.execute(update_user_query)
        self.connection.commit()

        # Get user and role
        select_user_role_query = f'''SELECT a.rolname AS user, c.rolname AS role FROM pg_catalog.pg_roles a INNER JOIN pg_catalog.pg_auth_members b ON a.oid=b.member INNER JOIN pg_catalog.pg_roles c ON b.roleid=c.oid WHERE a.rolname='{user}';'''
        cursor = self.connection.execute(select_user_role_query)
        self.connection.commit()
        row = cursor.fetchone()

        # Assert user was created and standard role granted
        self.assertEqual(row[0], user)
        self.assertEqual(row[1], 'admin')

    @classmethod
    def tearDownClass(cls):
        """Execute this at the end of the tests."""
        cls.connection.close()


if __name__ == '__main__':
    unittest.main()
