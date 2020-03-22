/*Connect to database*/
\connect mobydq



/*Create table data source type*/
CREATE TABLE base.data_source_type (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
);

COMMENT ON TABLE base.data_source_type IS
'Data source types describe the types of a data sources indicators can connect to.';

/*Triggers on update*/
CREATE TRIGGER data_source_type_update_updated_date BEFORE UPDATE
ON base.data_source_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER data_source_type_update_updated_by_id BEFORE UPDATE
ON base.data_source_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();



/*Triggers on delete*/
CREATE TRIGGER data_source_type_delete_data_source BEFORE DELETE
ON base.data_source_type FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('data_source', 'data_source_type_id');



/*Order matter since Id values will be generated accordingly, do not change it*/
INSERT INTO base.data_source_type (name) VALUES
  ('Cloudera Hive')
, ('Cloudera Impala')
, ('MariaDB')
, ('Microsoft SQL Server')
, ('MySQL')
, ('Oracle')
, ('PostgreSQL')
, ('SQLite')
, ('Teradata')
, ('Snowflake')
, ('Hortonworks Hive');
