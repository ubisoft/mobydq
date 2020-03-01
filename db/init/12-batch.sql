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
  , user_group_id INTEGER DEFAULT 1 REFERENCES base.user_group(id)
  , indicator_group_id INTEGER NOT NULL REFERENCES base.indicator_group(id)
);

COMMENT ON TABLE base.batch IS
'Batches record the execution of groups of indicators.';


/*Define list of values for batch status*/
ALTER TABLE base.batch
ADD CONSTRAINT check_types 
CHECK (status IN ('Pending', 'Running', 'Success', 'Failed', 'Killed'));



/*Triggers on update*/
CREATE TRIGGER batch_update_updated_date BEFORE UPDATE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER batch_update_updated_by_id BEFORE UPDATE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();

CREATE TRIGGER batch_update_send_update AFTER UPDATE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.send_update('batch');



/*Triggers on delete*/
CREATE TRIGGER batch_delete_session BEFORE DELETE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('session', 'batch_id');

CREATE TRIGGER batch_delete_log BEFORE DELETE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('log', 'batch_id');

CREATE TRIGGER batch_delete_notification BEFORE DELETE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('notification', 'batch_id');



/*Create function to execute batch of indicators*/
CREATE OR REPLACE FUNCTION base.execute_batch(indicator_group_id INTEGER, indicator_id INTEGER ARRAY DEFAULT '{}')
RETURNS base.batch AS $$
#variable_conflict use_variable
DECLARE
    batch base.batch;
BEGIN
    -- Create pending batch
    /*TODO: replace placeholder of column user_group_id*/
    INSERT INTO base.batch (status, indicator_group_id, user_group_id)
    VALUES ('Pending', indicator_group_id, 1)
    RETURNING * INTO batch;

    -- Create pending session for each indicator
    /*TODO: replace placeholder of column user_group_id*/
    IF indicator_id <> '{}' THEN
        WITH indicator AS (
            SELECT a.id
            FROM base.indicator a
            WHERE a.indicator_group_id=indicator_group_id
            AND a.flag_active=true
            AND a.id=ANY(indicator_id)
            ORDER BY a.execution_order
        ) INSERT INTO base.session (status, indicator_id, batch_id, user_group_id)
        SELECT 'Pending', indicator.id, batch.id, 1 FROM indicator;
    ELSE
        WITH indicator AS (
            SELECT a.id
            FROM base.indicator a
            WHERE a.indicator_group_id=indicator_group_id
            AND a.flag_active=true
            ORDER BY a.execution_order
        ) INSERT INTO base.session (status, indicator_id, batch_id, user_group_id)
        SELECT 'Pending', indicator.id, batch.id, 1 FROM indicator;
    END IF;
    -- Execution of indicators is triggered by the GraphQL API
    -- Return batch record
    RETURN batch;
END;
$$ LANGUAGE plpgsql VOLATILE STRICT SECURITY DEFINER;

COMMENT ON FUNCTION base.execute_batch IS
'Function used to execute a batch of indicators.';

REVOKE ALL ON FUNCTION base.execute_batch FROM PUBLIC;



/*Create function to kill batch of indicators*/
CREATE OR REPLACE FUNCTION base.kill_execute_batch(batch_id INTEGER)
RETURNS base.batch AS $$
#variable_conflict use_variable
DECLARE
    batch base.batch;
    existing_batch RECORD;
BEGIN
    -- Get existing batch
    SELECT id
    INTO existing_batch
    FROM base.batch
    WHERE id=batch_id
    AND status NOT IN ('Success', 'Failed', 'Killed');
    
    -- Verify if batch exists
    IF existing_batch.id IS NOT NULL THEN
        -- Update sessions status to Killed
        UPDATE base.session a
        SET status='Killed'
        WHERE a.batch_id=batch_id
        AND a.status NOT IN ('Success', 'Failed', 'Killed');

        -- Update batch status to Killed
        UPDATE base.batch
        SET status='Killed'
        WHERE id=batch_id
        RETURNING * INTO batch;
    ELSE
        RAISE EXCEPTION 'Batch Id % does not exist or status is already Success, Failed or Killed.', batch_id;
    END IF;

    RETURN batch;
END;
$$ LANGUAGE plpgsql VOLATILE STRICT SECURITY DEFINER;

COMMENT ON FUNCTION base.kill_execute_batch IS
'Function used to kill a batch of indicators.';

REVOKE ALL ON FUNCTION base.kill_execute_batch FROM PUBLIC;