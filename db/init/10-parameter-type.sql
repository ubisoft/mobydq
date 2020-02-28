/*Connect to database*/
\connect mobydq



/*Create table parameter type*/
CREATE TABLE base.parameter_type (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , description TEXT
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
);

COMMENT ON TABLE base.parameter_type IS
'Parameter types determine which types of parameters can be used to compute indicators.';



/*Triggers on update*/
CREATE TRIGGER parameter_type_update_updated_date BEFORE UPDATE
ON base.parameter_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER parameter_type_update_updated_by_id BEFORE UPDATE
ON base.parameter_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();



/*Triggers on delete*/
CREATE TRIGGER parameter_type_delete_parameter BEFORE DELETE
ON base.parameter_type FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('parameter', 'parameter_type_id');



/*Order matter since Id values will be generated accordingly, do not change it*/
INSERT INTO base.parameter_type (name, description) VALUES
  ('Alert operator', 'Operator used to compare the results of the indicator with the alert threshold. Example: ==, >, >=, <, <=, <>')
, ('Alert threshold', 'Numeric value used to evaluate the results of the indicator and determine if an alert must be sent.')
, ('Distribution list', 'List of e-mail addresses to which alerts must be sent. Example: [''email_1'', ''email_2'', ''email_3'']')
, ('Dimension', 'List of values to indicate dimensions in the results of the indicator. Example: [''dimension_1'', ''dimension_2'', ''dimension_3'']')
, ('Measure', 'List of values to indicate measures in the results of the indicator. Example: [''measure_1'', ''measure_2'', ''measure_3'']')
, ('Source', 'Name of the data source which serves as a reference to evaluate the quality of the data.')
, ('Source request', 'SQL query used to compute the indicator on the source system.')
, ('Target', 'Name of the data source on which to evaluate the quality of the data.')
, ('Target request', 'SQL query used to compute the indicator on the target system.');
