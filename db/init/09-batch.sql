/*Connect to database*/
\connect mobydq



/*Create table batch*/
CREATE TABLE base.batch (
    id SERIAL PRIMARY KEY
  , status TEXT NOT NULL
  , user_group TEXT NOT NULL
  , created_by TEXT DEFAULT CURRENT_USER
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_by TEXT DEFAULT CURRENT_USER
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



/*Create function to execute batch of indicators*/
CREATE OR REPLACE FUNCTION base.execute_batch(indicator_group_id INTEGER, indicator_id INTEGER ARRAY DEFAULT NULL)
RETURNS base.batch AS $$
#variable_conflict use_variable
DECLARE
    batch base.batch;
BEGIN
    -- Create pending batch
    /*TODO: replace placeholder of column user_group*/
    INSERT INTO base.batch (status, indicator_group_id, user_group)
    VALUES ('Pending', indicator_group_id, '')
    RETURNING * INTO batch;

    -- Create pending session for each indicator
    /*TODO: replace placeholder of column user_group*/
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
