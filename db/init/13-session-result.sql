/*Connect to database*/
\connect mobydq



/*Create table session result*/
CREATE TABLE base.session_result (
    id SERIAL PRIMARY KEY
  , alert_operator TEXT NOT NULL
  , alert_threshold FLOAT NOT NULL
  , nb_records INTEGER NOT NULL
  , nb_records_alert INTEGER NOT NULL
  , nb_records_no_alert INTEGER NOT NULL
  , user_group TEXT NOT NULL
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , session_id INTEGER NOT NULL REFERENCES base.session(id)
);

COMMENT ON TABLE base.session_result IS
'Session results contain a summary of indicators execution.';
