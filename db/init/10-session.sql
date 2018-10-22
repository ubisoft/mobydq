/*Connect to database*/
\connect mobydq



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
