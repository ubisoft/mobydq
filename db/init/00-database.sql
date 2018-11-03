/*Connect to database*/
\connect mobydq

/*Create schema*/
CREATE SCHEMA configuration;

/*Create table user group*/
CREATE TABLE configuration.parameter (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , value TEXT
);

COMMENT ON TABLE configuration.parameter IS
'Configuration parameters.';



/*Create schema*/
CREATE SCHEMA base;

/*Install pgcrypto exstension to encrypt/decrypt data sources passwords*/
CREATE EXTENSION IF NOT EXISTS pgcrypto;

/*Create function to update updated_date column*/
CREATE OR REPLACE FUNCTION base.update_updated_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_date = now();
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.update_updated_date IS
'Function used to automatically update the updated_date column in tables.';



/*Create function to delete children record*/
CREATE OR REPLACE FUNCTION base.delete_children()
RETURNS TRIGGER AS $$
DECLARE
    children_table TEXT;
    parent_column TEXT;
    parent_value INTEGER;
BEGIN
    children_table = TG_ARGV[0];
    parent_column = TG_ARGV[1];
    parent_value = OLD.id;
    EXECUTE 'DELETE FROM base.' || children_table || ' WHERE ' || parent_column || '=' || parent_value;
    RETURN OLD;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.delete_children IS
'Function used to automate cascade delete on children tables.';
