/*Connect to database*/
\connect mobydq



/*Create table indicator type*/
CREATE TABLE base.indicator_type (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , module TEXT NOT NULL
  , class TEXT NOT NULL
  , method TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
);

COMMENT ON TABLE base.indicator_type IS
'Indicator types determine which class and method is used to compute indicators.';



/*Triggers on update*/
CREATE TRIGGER indicator_type_update_updated_date BEFORE UPDATE
ON base.indicator_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER indicator_type_update_updated_by_id BEFORE UPDATE
ON base.indicator_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();



/*Triggers on delete*/
CREATE TRIGGER indicator_type_delete_indicator BEFORE DELETE
ON base.indicator_type FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('indicator', 'indicator_type_id');



/*Order matter since Id values will be generated accordingly, do not change it*/
INSERT INTO base.indicator_type (name, module, class, method) VALUES
  ('Completeness', 'completeness', 'Completeness', 'execute')
, ('Freshness', 'freshness', 'Freshness', 'execute')
, ('Latency', 'latency', 'Latency', 'execute')
, ('Validity', 'validity', 'Validity', 'execute');
