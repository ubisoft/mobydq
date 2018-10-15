/*Create database*/
CREATE DATABASE mobydq;
\connect mobydq;

/*Create schema*/
CREATE SCHEMA base;



/*Create function to update updated_date column*/
CREATE OR REPLACE FUNCTION base.update_updated_date_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_date = now();
   RETURN NEW;
END;
$$ language plpgsql;
COMMENT ON FUNCTION base.update_updated_date_column IS
'Function used to automatically update the updated_date column in tables.';



/*Create function to delete children record*/
CREATE OR REPLACE FUNCTION base.delete_children()
RETURNS TRIGGER AS $$
DECLARE
    children_table TEXT;
    parent_column TEXT;
    parent_value INTEGER;
BEGIN
    children_table = TG_ARGV[0];
    parent_column = TG_ARGV[1];
    parent_value = OLD.id;
    EXECUTE('DELETE FROM base.' || children_table || ' WHERE ' || parent_column || '=' || parent_value || ';');
    RETURN OLD;
END;
$$ language plpgsql;
COMMENT ON FUNCTION base.delete_children IS
'Function used to automate cascade delete on children tables.';



/*Create table data source type*/
CREATE TABLE base.data_source_type (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE base.data_source_type IS
'Data source types describe the types of a data sources indicators can connect to.';

CREATE TRIGGER data_source_type_updated_date BEFORE UPDATE
ON base.data_source_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

CREATE TRIGGER data_source_type_delete_data_source BEFORE DELETE
ON base.data_source_type FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('data_source', 'data_source_type_id');



/*Create table data source*/
CREATE TABLE base.data_source (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , connection_string TEXT
  , login TEXT
  , password TEXT
  , connectivity_status TEXT
  , user_group TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , data_source_type_id INTEGER NOT NULL REFERENCES base.data_source_type(id)
);
COMMENT ON TABLE base.data_source IS
'Data sources are systems containing or exposing data on which to compute indicators.';

CREATE TRIGGER data_source_updated_date BEFORE UPDATE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

ALTER TABLE base.data_source ENABLE ROW LEVEL SECURITY;



/*Create table indicator type*/
CREATE TABLE base.indicator_type (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , module TEXT NOT NULL
  , class TEXT NOT NULL
  , method TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE base.indicator_type IS
'Indicator types determine which class and method is used to compute indicators.';

CREATE TRIGGER indicator_type_updated_date BEFORE UPDATE
ON base.indicator_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

CREATE TRIGGER indicator_type_delete_indicator BEFORE DELETE
ON base.indicator_type FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('indicator', 'indicator_type_id');



/*Create table indicator group*/
CREATE TABLE base.indicator_group (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , user_group TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE base.indicator_group IS
'Indicator groups define collections of indicators to be computed in the same batch.';

CREATE TRIGGER indicator_group_updated_date BEFORE UPDATE
ON base.indicator_group FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

CREATE TRIGGER indicator_group_delete_indicator BEFORE DELETE
ON base.indicator_group FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('indicator', 'indicator_group_id');

ALTER TABLE base.indicator_group ENABLE ROW LEVEL SECURITY;



/*Create table indicator*/
CREATE TABLE base.indicator (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , description TEXT
  , execution_order INTEGER DEFAULT 0
  , flag_active BOOLEAN DEFAULT FALSE
  , user_group TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , indicator_type_id INTEGER NOT NULL REFERENCES base.indicator_type(id)
  , indicator_group_id INTEGER NOT NULL REFERENCES base.indicator_group(id)
);
COMMENT ON TABLE base.indicator IS
'Indicators compute data sets on one or several data sources in order to evaluate the quality of their data.';

CREATE TRIGGER indicator_updated_date BEFORE UPDATE
ON base.indicator FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

CREATE TRIGGER indicator_delete_parameter BEFORE DELETE
ON base.indicator FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('parameter', 'indicator_id');

CREATE TRIGGER indicator_delete_session BEFORE DELETE
ON base.indicator FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('session', 'indicator_id');

ALTER TABLE base.indicator ENABLE ROW LEVEL SECURITY;



/*Create table parameter type*/
CREATE TABLE base.parameter_type (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , description TEXT
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE base.parameter_type IS
'Parameter types determine which types of parameters can be used to compute indicators.';

CREATE TRIGGER parameter_type_updated_date BEFORE UPDATE
ON base.parameter_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

CREATE TRIGGER parameter_type_delete_parameter BEFORE DELETE
ON base.parameter_type FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('parameter', 'parameter_type_id');



/*Create table parameter*/
CREATE TABLE base.parameter (
    id SERIAL PRIMARY KEY
  , value TEXT NOT NULL
  , user_group TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , parameter_type_id INTEGER NOT NULL REFERENCES base.parameter_type(id)
  , indicator_id INTEGER NOT NULL REFERENCES base.indicator(id)
  , CONSTRAINT parameter_unicity UNIQUE (indicator_id, parameter_type_id)
);
COMMENT ON TABLE base.parameter IS
'Parameters used to compute indicators.';

CREATE TRIGGER parameter_updated_date BEFORE UPDATE
ON base.parameter FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

ALTER TABLE base.parameter ENABLE ROW LEVEL SECURITY;



/*Create table batch*/
CREATE TABLE base.batch (
    id SERIAL PRIMARY KEY
  , status TEXT NOT NULL
  , user_group TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , indicator_group_id INTEGER NOT NULL REFERENCES base.indicator_group(id)
);
COMMENT ON TABLE base.batch IS
'Batches record the execution of groups of indicators.';

CREATE TRIGGER batch_updated_date BEFORE UPDATE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

CREATE TRIGGER batch_delete_session BEFORE DELETE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('session', 'batch_id');

ALTER TABLE base.batch ENABLE ROW LEVEL SECURITY;



/*Create table session*/
CREATE TABLE base.session (
    id SERIAL PRIMARY KEY
  , status TEXT NOT NULL
  , user_group TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , batch_id INTEGER NOT NULL REFERENCES base.batch(id)
  , indicator_id INTEGER NOT NULL REFERENCES base.indicator(id)
);
COMMENT ON TABLE base.session IS
'Sessions record the execution of indicators within a batch.';

CREATE TRIGGER session_updated_date BEFORE UPDATE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

CREATE TRIGGER session_delete_session_result BEFORE DELETE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('session_result', 'session_id');

ALTER TABLE base.session ENABLE ROW LEVEL SECURITY;



/*Create table session result*/
CREATE TABLE base.session_result (
    id SERIAL PRIMARY KEY
  , alert_operator TEXT NOT NULL
  , alert_threshold FLOAT NOT NULL
  , nb_records INTEGER NOT NULL
  , nb_records_alert INTEGER NOT NULL
  , nb_records_no_alert INTEGER NOT NULL
  , user_group TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , session_id INTEGER NOT NULL REFERENCES base.session(id)
);
COMMENT ON TABLE base.session_result IS
'Session results contain a summary of indicators execution.';

ALTER TABLE base.session_result ENABLE ROW LEVEL SECURITY;


/*Create table user*/
CREATE TABLE base.user (
    id SERIAL PRIMARY KEY
  , email TEXT NOT NULL UNIQUE
  , flag_active BOOLEAN DEFAULT TRUE
  , oauth_type TEXT NOT NULL
  , access_token TEXT NOT NULL
  , refresh_token INTEGER
  , expiry_date TIMESTAMP NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE base.user IS
'User contains information about user and his authentication.';

CREATE TRIGGER batch_updated_date BEFORE UPDATE
ON base.user FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();



/*TODO: create view on pg_roles*/



/*Create function to execute indicator group*/
CREATE OR REPLACE FUNCTION base.execute_batch(indicator_group_id INTEGER, indicator_id INTEGER ARRAY DEFAULT NULL)
RETURNS base.batch AS $$
#variable_conflict use_variable
DECLARE
    batch base.batch;
BEGIN
    -- Create pending batch
    /*TOOD: replace placeholder of column user_group*/
    INSERT INTO base.batch (status, indicator_group_id, user_group)
    VALUES ('Pending', indicator_group_id, '')
    RETURNING * INTO batch;

    -- Create pending session for each indicator
    /*TOOD: replace placeholder of column user_group*/
    IF indicator_id IS NOT NULL THEN
        WITH indicator AS (
            SELECT a.id
            FROM base.indicator a
            WHERE a.indicator_group_id=indicator_group_id
            AND a.flag_active=true
            AND a.id=ANY(indicator_id)
            ORDER BY a.execution_order
        ) INSERT INTO base.session (status, indicator_id, batch_id, user_group)
        SELECT 'Pending', indicator.id, batch.id, '' FROM indicator;
    ELSE
        WITH indicator AS (
            SELECT a.id
            FROM base.indicator a
            WHERE a.indicator_group_id=indicator_group_id
            AND a.flag_active=true
            ORDER BY a.execution_order
        ) INSERT INTO base.session (status, indicator_id, batch_id, user_group)
        SELECT 'Pending', indicator.id, batch.id, '' FROM indicator;
    END IF;
    -- Executions of indicators are triggered by the Flask API
    -- Return batch record
    RETURN batch;
END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;
COMMENT ON FUNCTION base.execute_batch IS
'Function used to execute a batch of indicators.';



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



/*Create function to duplicate an indicator*/
CREATE OR REPLACE FUNCTION base.duplicate_indicator(indicator_id INTEGER, new_indicator_name TEXT)
RETURNS base.indicator AS $$
#variable_conflict use_variable
DECLARE
    indicator base.indicator;
BEGIN
    -- Duplicate indicator
    INSERT INTO base.indicator (name, description, execution_order, flag_active, indicator_type_id, indicator_group_id, user_group)
    SELECT new_indicator_name, a.description, a.execution_order, a.flag_active, a.indicator_type_id, a.indicator_group_id, a.user_group
    FROM base.indicator a
    WHERE a.id=indicator_id
    RETURNING * INTO indicator;

    -- Duplicate parameters
    INSERT INTO base.parameter (value, parameter_type_id, indicator_id, user_group)
    SELECT a.value, a.parameter_type_id, indicator.id, a.user_group
    FROM base.parameter a
    WHERE a.indicator_id=indicator_id;

    RETURN indicator;
END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;
COMMENT ON FUNCTION base.duplicate_indicator IS
'Function used to duplicate an indicator.';



/*Create function to create a new user group role and its grants and policies */
CREATE OR REPLACE FUNCTION base.create_new_user_group(user_group_name TEXT)
RETURNS VOID AS $$
DECLARE
    new_user_group                     TEXT := 'user_group_' || user_group_name;
    new_user_group_admin               TEXT := new_user_group || '_admin';
    indicator_group_group_all_policy   TEXT := new_user_group || '_indicator_group_all';
    indicator_group_all_policy         TEXT := new_user_group || '_indicator_all';
    parameter_group_all_policy         TEXT := new_user_group || '_parameter_all';
    data_source_group_select_policy    TEXT := new_user_group || '_data_source_select';
    data_source_admin_all_policy       TEXT := new_user_group_admin || '_data_source_all';
    session_group_select_policy        TEXT := new_user_group || '_session_select';
    session_result_group_select_policy TEXT := new_user_group || '_session_result_select';
    batch_group_select_policy          TEXT := new_user_group || '_batch_all';
BEGIN

    EXECUTE 'CREATE ROLE ' || quote_ident(new_user_group);
    EXECUTE 'CREATE ROLE ' || quote_ident(new_user_group_admin);
    EXECUTE 'GRANT ' || quote_ident(new_user_group) || ' TO ' || quote_ident(new_user_group_admin);

    EXECUTE 'GRANT ALL    ON base.indicator_group
                  , base.indicator
                  , base.parameter
    TO'  || quote_ident(new_user_group);
    EXECUTE 'GRANT SELECT ON base.data_source
                  , base.data_source_type
                  , base.parameter_type
                  , base.indicator_type
                  , base.batch
                  , base.session
                  , base.session_result
    TO ' || quote_ident(new_user_group);
    EXECUTE 'GRANT ALL    ON base.data_source
    TO ' || quote_ident(new_user_group_admin);

    /*policy for indicator_group*/
    EXECUTE 'CREATE POLICY ' || quote_ident(indicator_group_group_all_policy) || ' ON
      base.indicator_group
    FOR ALL
    TO ' || quote_ident(new_user_group) || '
    USING (
      user_group = ''' || new_user_group || '''
    )';

    /*policy for indicator*/
    EXECUTE 'CREATE POLICY ' || quote_ident(indicator_group_all_policy) || ' ON
      base.indicator
    FOR ALL
    TO' || quote_ident(new_user_group) || '
    USING (
      user_group = ''' || new_user_group ||'''
    )';

    /*policy for parameter*/
    EXECUTE 'CREATE POLICY ' || quote_ident(parameter_group_all_policy) || ' ON
      base.parameter
    FOR ALL
    TO ' || quote_ident(new_user_group) || '
    USING (
      user_group = ''' || new_user_group || '''
    )';

    /*policies for data_source*/
    EXECUTE 'CREATE POLICY ' || quote_ident(data_source_group_select_policy) || ' ON
      base.data_source
    FOR SELECT
    TO ' || quote_ident(new_user_group) || '
    USING (
      user_group = ''' || new_user_group || '''
    )';

    EXECUTE 'CREATE POLICY ' || quote_ident(data_source_admin_all_policy) || ' ON
      base.data_source
    FOR ALL
    TO ' || quote_ident(new_user_group_admin) || '
    USING (
      user_group = ''' || new_user_group_admin || '''
    )';

    /*policy for session*/
    EXECUTE 'CREATE POLICY ' || quote_ident(session_group_select_policy) || ' ON
      base.session
    FOR SELECT
    TO ' || quote_ident(new_user_group) || '
    USING (
      user_group = ''' || new_user_group || '''
    )';

    /*policy for session_result*/
    EXECUTE 'CREATE POLICY ' || quote_ident(session_result_group_select_policy) || ' ON
      base.session_result
    FOR SELECT
    TO ' || quote_ident(new_user_group) || '
    USING (
      user_group = ''' || new_user_group || '''
    )';

    /*policy for batch*/
    EXECUTE 'CREATE POLICY '  || quote_ident(batch_group_select_policy) || ' ON
      base.batch
    FOR SELECT
    TO ' || quote_ident(new_user_group) || '
    USING (
      user_group = ''' || new_user_group || '''
    )';

END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;
COMMENT ON FUNCTION base.create_new_user_group IS
'Function used to create new user group role and new policies for a group and group admin role.';
