/*Connect to database*/
\connect mobydq



/*Create table user group*/
CREATE TABLE base.user_group (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
);

COMMENT ON TABLE base.user_group IS
'User groups are used to managed visibility rules at record level.';

CREATE TRIGGER user_group_update_updated_date BEFORE UPDATE
ON base.user_group FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER user_group_update_updated_by_id BEFORE UPDATE
ON base.user_group FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();

CREATE TRIGGER user_group_delete_user_group_user BEFORE DELETE
ON base.user_group FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('user_group_user', 'user_group_id');



/*Create function to create database user group in pg_roles table when user group is created in user_group table*/
CREATE OR REPLACE FUNCTION base.create_user_group()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE 'CREATE ROLE user_group_' || NEW.id;
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.create_user_group IS
'Function used to automatically create database user group in pg_roles table when user group is created in user_group table.';

CREATE TRIGGER user_group_create_user_group AFTER INSERT
ON base.user_group FOR EACH ROW EXECUTE PROCEDURE
base.create_user_group();



/*Create function to delete database user group in pg_roles table when user group is deleted in user_group table*/
CREATE OR REPLACE FUNCTION base.delete_user_group()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE 'DROP ROLE IF EXISTS user_group_' || OLD.id;
    RETURN OLD;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.delete_user_group IS
'Function used to automatically delete database user group in pg_roles table when user group is deleted in user_group table.';

CREATE TRIGGER user_group_delete_user_group AFTER DELETE
ON base.user_group FOR EACH ROW EXECUTE PROCEDURE
base.delete_user_group();



/*Create default user group*/
INSERT INTO base.user_group (name) VALUES ('Public');
