/*Connect to database*/
\connect mobydq



/*Create table data source type*/
CREATE TABLE base.data_source_type (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , created_by TEXT DEFAULT CURRENT_USER
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_by TEXT DEFAULT CURRENT_USER
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE base.data_source_type IS
'Data source types describe the types of a data sources indicators can connect to.';

CREATE TRIGGER data_source_type_updated_date BEFORE UPDATE
ON base.data_source_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

CREATE TRIGGER data_source_type_delete_data_source BEFORE DELETE
ON base.data_source_type FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('data_source', 'data_source_type_id');



/*Order matter since Id values will be generated accordingly, do not change it*/
INSERT INTO base.data_source_type (name) VALUES
  ('Hive')
, ('Impala')
, ('MariaDB')
, ('Microsoft SQL Server')
, ('MySQL')
, ('Oracle')
, ('PostgreSQL')
, ('SQLite')
, ('Teradata');
