/*Connect to database*/
\connect mobydq



/*Create table parameter*/
CREATE TABLE base.parameter (
    id SERIAL PRIMARY KEY
  , value TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , user_group_id INTEGER DEFAULT 1 REFERENCES base.user_group(id)
  , indicator_id INTEGER NOT NULL REFERENCES base.indicator(id)
  , parameter_type_id INTEGER NOT NULL REFERENCES base.parameter_type(id)
  , CONSTRAINT parameter_uniqueness UNIQUE (indicator_id, parameter_type_id)
);

COMMENT ON TABLE base.parameter IS
'Parameters used to compute indicators.';



/*Triggers on update*/
CREATE TRIGGER parameter_update_updated_date BEFORE UPDATE
ON base.parameter FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER parameter_update_updated_by_id BEFORE UPDATE
ON base.parameter FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();
