/*Connect to database*/
\connect mobydq



/*Create table user group*/
CREATE TABLE base.user_group (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE base.user_group IS
'User groups are used to managed visibility rules.';

CREATE TRIGGER user_group_updated_date BEFORE UPDATE
ON base.user_group FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();



/*Create function to create user group role*/
CREATE OR REPLACE FUNCTION base.create_user_group_role()
RETURNS TRIGGER AS $$
DECLARE
    user_group TEXT := 'user_group_' || NEW.id;
BEGIN
    EXECUTE 'CREATE ROLE ' || user_group;
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.create_user_group_role IS
'Function used to automatically create a role for a user group.';

CREATE TRIGGER user_group_create_user_group_role AFTER INSERT
ON base.user_group FOR EACH ROW EXECUTE PROCEDURE
base.create_user_group_role();
