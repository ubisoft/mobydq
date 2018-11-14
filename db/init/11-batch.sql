/*Connect to database*/
\connect mobydq



/*Create table batch*/
CREATE TABLE base.batch (
    id SERIAL PRIMARY KEY
  , status TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , user_group_id INTEGER DEFAULT 0 REFERENCES base.user_group(id)
  , indicator_group_id INTEGER NOT NULL REFERENCES base.indicator_group(id)
);

COMMENT ON TABLE base.batch IS
'Batches record the execution of groups of indicators.';

CREATE TRIGGER batch_update_updated_date BEFORE UPDATE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER batch_update_updated_by_id BEFORE UPDATE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();

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
    /*TODO: replace placeholder of column user_group_id*/
    INSERT INTO base.batch (status, indicator_group_id, user_group_id)
    VALUES ('Pending', indicator_group_id, 0)
    RETURNING * INTO batch;

    -- Create pending session for each indicator
    /*TODO: replace placeholder of column user_group_id*/
    IF indicator_id IS NOT NULL THEN
        WITH indicator AS (
            SELECT a.id
            FROM base.indicator a
            WHERE a.indicator_group_id=indicator_group_id
            AND a.flag_active=true
            AND a.id=ANY(indicator_id)
            ORDER BY a.execution_order
        ) INSERT INTO base.session (status, indicator_id, batch_id, user_group_id)
        SELECT 'Pending', indicator.id, batch.id, 0 FROM indicator;
    ELSE
        WITH indicator AS (
            SELECT a.id
            FROM base.indicator a
            WHERE a.indicator_group_id=indicator_group_id
            AND a.flag_active=true
            ORDER BY a.execution_order
        ) INSERT INTO base.session (status, indicator_id, batch_id, user_group_id)
        SELECT 'Pending', indicator.id, batch.id, 0 FROM indicator;
    END IF;
    -- Executions of indicators are triggered by the Flask API
    -- Return batch record
    RETURN batch;
END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;

COMMENT ON FUNCTION base.execute_batch IS
'Function used to execute a batch of indicators.';
