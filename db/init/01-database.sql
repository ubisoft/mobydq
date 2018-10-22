/*Create database*/
CREATE DATABASE mobydq;
\connect mobydq;

/*Create schema*/
CREATE SCHEMA base;



/*Create function to update updated_date column*/
CREATE OR REPLACE FUNCTION base.update_updated_date_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_date = now();
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.update_updated_date_column IS
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



/*Create function to delete role*/
CREATE OR REPLACE FUNCTION base.delete_role()
RETURNS TRIGGER AS $$
DECLARE
    role_name TEXT;
BEGIN
    role_name = TG_ARGV[0];
    EXECUTE 'DROP ROLE IF EXISTS ' || role_name;
    RETURN OLD;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.delete_role IS
'Function used to automate cascade delete of a role.';
