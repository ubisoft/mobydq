/*Connect to database*/
\connect mobydq



/*Create table data source*/
CREATE TABLE base.data_source (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , connection_string TEXT
  , login TEXT
  , password TEXT
  , connectivity_status TEXT
  , user_group TEXT NOT NULL
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , data_source_type_id INTEGER NOT NULL REFERENCES base.data_source_type(id)
);

COMMENT ON TABLE base.data_source IS
'Data sources are systems containing or exposing data on which to compute indicators.';

CREATE TRIGGER data_source_update_updated_date BEFORE UPDATE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER data_source_update_updated_by_id BEFORE UPDATE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();



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
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;

COMMENT ON FUNCTION base.test_data_source IS
'Function used to test connectivity to a data source.';
