/*Connect to database*/
\connect mobydq



/*Create a secret key to encrypt data source passwords*/
INSERT INTO base.configuration (name, value) VALUES ('secret_key', MD5(random()::text));



/*Create function to encrypt password column*/
CREATE OR REPLACE FUNCTION base.encrypt_password()
RETURNS TRIGGER AS $$
BEGIN
    NEW.password = PGP_SYM_ENCRYPT(NEW.password, (SELECT value FROM base.configuration WHERE name = 'secret_key'));
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.encrypt_password IS
'Function used to encrypt password column in data source table.';



/*Create table data source*/
CREATE TABLE base.data_source (
    id SERIAL PRIMARY KEY
  , name CITEXT NOT NULL UNIQUE
  , connection_string TEXT NOT NULL
  , login TEXT
  , password TEXT
  , connectivity_status TEXT
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , user_group_id INTEGER DEFAULT 1 REFERENCES base.user_group(id)
  , data_source_type_id INTEGER NOT NULL REFERENCES base.data_source_type(id)
);

COMMENT ON TABLE base.data_source IS
'Data sources are systems containing or exposing data on which to compute indicators.';



/*Triggers on insert*/
CREATE TRIGGER data_source_insert_password BEFORE INSERT
ON base.data_source FOR EACH ROW WHEN (NEW.password IS NOT NULL) EXECUTE PROCEDURE
base.encrypt_password();



/*Triggers on update*/
CREATE TRIGGER data_source_update_password BEFORE UPDATE OF password
ON base.data_source FOR EACH ROW WHEN (NEW.password IS NOT NULL)
EXECUTE PROCEDURE base.encrypt_password();

CREATE TRIGGER data_source_update_updated_date BEFORE UPDATE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER data_source_update_updated_by_id BEFORE UPDATE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();

CREATE TRIGGER data_source_update_send AFTER UPDATE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.send_update('dataSource');



/*Triggers on delete*/
CREATE TRIGGER data_source_delete_log BEFORE DELETE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('log', 'data_source_id');

CREATE TRIGGER data_source_delete_notification BEFORE DELETE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('notification', 'data_source_id');



/*Create function to search data sources*/
CREATE OR REPLACE FUNCTION base.search_data_source(search_keyword TEXT, sort_attribute TEXT, sort_order TEXT)
RETURNS SETOF base.data_source AS $$
BEGIN
    RETURN QUERY
    EXECUTE format(
        'SELECT a.*
        FROM base.data_source a
        WHERE a.name ILIKE (''%%%s%%'')
        ORDER BY a.%I %s',
        search_keyword,
        sort_attribute,
        sort_order);
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.search_data_source IS
'Function used to search data sources based on keywords contained in their name.';



/*Create view to decrypt data source password column*/
CREATE OR REPLACE VIEW base.data_source_password
AS SELECT id, PGP_SYM_DECRYPT(password::bytea, (SELECT value FROM base.configuration WHERE name = 'secret_key')) AS password
FROM base.data_source;

COMMENT ON VIEW base.data_source_password IS
E'@omit create\nView used to decrypt the password of a data source.';



/*Create function to test connectivity to a data source*/
CREATE OR REPLACE FUNCTION base.test_data_source(data_source_id INTEGER)
RETURNS base.data_source AS $$
#variable_conflict use_variable
DECLARE
    data_source base.data_source;
BEGIN
    -- Update data source connectivity status to Pending
    UPDATE base.data_source
    SET connectivity_status='Pending'
    WHERE id=data_source_id
    RETURNING * INTO data_source;
    RETURN data_source;
END;
$$ LANGUAGE plpgsql VOLATILE STRICT SECURITY DEFINER;

COMMENT ON FUNCTION base.test_data_source IS
'Function used to test connectivity to a data source.';

REVOKE ALL ON FUNCTION base.test_data_source FROM PUBLIC;



/*Create function to kill test of a data source*/
CREATE OR REPLACE FUNCTION base.kill_test_data_source(data_source_id INTEGER)
RETURNS base.data_source AS $$
#variable_conflict use_variable
DECLARE
    data_source base.data_source;
    existing_data_source RECORD;
BEGIN
    -- Get existing data source
    SELECT id
    INTO existing_data_source
    FROM base.data_source
    WHERE id=data_source_id
    AND connectivity_status NOT IN ('Success', 'Failed', 'Killed');
    
    -- Verify if data source exists
    IF existing_data_source.id IS NOT NULL THEN
        -- Update connectivity status to Killed
        UPDATE base.data_source
        SET connectivity_status='Killed'
        WHERE id=data_source_id
        RETURNING * INTO data_source;
    ELSE
        RAISE EXCEPTION 'Data source Id % does not exist or connectivity status is already Success, Failed or Killed.', data_source_id;
    END IF;

    RETURN data_source;
END;
$$ LANGUAGE plpgsql VOLATILE STRICT SECURITY DEFINER;

COMMENT ON FUNCTION base.kill_test_data_source IS
'Function used to kill a test of a data source.';

REVOKE ALL ON FUNCTION base.kill_test_data_source FROM PUBLIC;