/*Connect to database*/
\connect mobydq



/*Create table parameter*/
CREATE TABLE base.parameter (
    id SERIAL PRIMARY KEY
  , value TEXT NOT NULL
  , user_group TEXT NOT NULL
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , parameter_type_id INTEGER NOT NULL REFERENCES base.parameter_type(id)
  , indicator_id INTEGER NOT NULL REFERENCES base.indicator(id)
  , CONSTRAINT parameter_uniqueness UNIQUE (indicator_id, parameter_type_id)
);

COMMENT ON TABLE base.parameter IS
'Parameters used to compute indicators.';

CREATE TRIGGER parameter_update_updated_date BEFORE UPDATE
ON base.parameter FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER parameter_update_updated_by_id BEFORE UPDATE
ON base.parameter FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();
