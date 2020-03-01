/*Connect to database*/
\connect mobydq



/*Create table session*/
CREATE TABLE base.session (
    id SERIAL PRIMARY KEY
  , status TEXT NOT NULL
  , alert_operator TEXT NULL
  , alert_threshold FLOAT NULL
  , nb_records INTEGER NULL
  , nb_records_alert INTEGER NULL
  , nb_records_no_alert INTEGER NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , user_group_id INTEGER DEFAULT 1 REFERENCES base.user_group(id)
  , batch_id INTEGER NOT NULL REFERENCES base.batch(id)
  , indicator_id INTEGER NOT NULL REFERENCES base.indicator(id)
);

COMMENT ON TABLE base.session IS
'Sessions record the execution of indicators within a batch.';



/*Define list of values for batch status*/
ALTER TABLE base.session
ADD CONSTRAINT check_types 
CHECK (status IN ('Pending', 'Running', 'Success', 'Failed', 'Killed'));



/*Triggers on update*/
CREATE TRIGGER session_update_updated_date BEFORE UPDATE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER session_update_updated_by_id BEFORE UPDATE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();

CREATE TRIGGER session_update_send_update AFTER UPDATE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.send_update('session');



/*Triggers on delete*/
CREATE TRIGGER session_delete_log BEFORE DELETE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('log', 'session_id');



/*Create function to search sessions*/
CREATE OR REPLACE FUNCTION base.search_session(search_keyword TEXT, sort_attribute TEXT, sort_order TEXT)
RETURNS SETOF base.session AS $$
BEGIN
    RETURN QUERY
    EXECUTE format(
        'SELECT a.*
        FROM base.session a
        INNER JOIN base.indicator b ON a.indicator_id=b.id
        WHERE b.name ILIKE (''%%%s%%'')
        ORDER BY a.%I %s',
        search_keyword,
        sort_attribute,
        sort_order);
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.search_session IS
'Function used to search sessions based on id or keywords contained in their indicator name.';