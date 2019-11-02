/*Connect to database*/
\connect mobydq



/*Create table session*/
CREATE TABLE base.session (
    id SERIAL PRIMARY KEY
  , status TEXT NOT NULL
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

CREATE TRIGGER session_update_updated_date BEFORE UPDATE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER session_update_updated_by_id BEFORE UPDATE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();

CREATE TRIGGER session_delete_session_result BEFORE DELETE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('session_result', 'session_id');
