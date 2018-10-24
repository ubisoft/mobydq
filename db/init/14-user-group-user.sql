/*Connect to database*/
\connect mobydq



/*Create table user group*/
CREATE TABLE base.user_group_user (
    id SERIAL PRIMARY KEY
  , user_group_id INTEGER NOT NULL REFERENCES base.user_group(id)
  , user_id INTEGER NOT NULL REFERENCES base.user(id)
  , created_by TEXT DEFAULT CURRENT_USER
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , CONSTRAINT user_group_user_uniqueness UNIQUE (user_group_id, user_id)
);

COMMENT ON TABLE base.user_group IS
'User groups users shows which user groups users are members of.';



/*Create function to grant user group role to user*/
CREATE OR REPLACE FUNCTION base.grant_user_group_role()
RETURNS TRIGGER AS $$
DECLARE
    user_group TEXT := 'user_group_' || NEW.user_group_id;
    user_role TEXT := 'user_' || NEW.user_id;
BEGIN
    EXECUTE 'GRANT ' || user_group || ' TO ' || user_role;
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.create_user_group_role IS
'Function used to automatically grant a user group role to a user.';

CREATE TRIGGER user_group_user_grant_user_group_role AFTER INSERT
ON base.user_group_user FOR EACH ROW EXECUTE PROCEDURE
base.grant_user_group_role();



/*Create function to revoke user group role to user*/
CREATE OR REPLACE FUNCTION base.revoke_user_group_role()
RETURNS TRIGGER AS $$
DECLARE
    user_group TEXT := 'user_group_' || OLD.user_group_id;
    user_role TEXT := 'user_' || OLD.user_id;
BEGIN
    EXECUTE 'REVOKE ' || user_group || ' FROM ' || user_role;
    RETURN OLD;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.revoke_user_group_role IS
'Function used to automatically revoke a user group role from a user.';

CREATE TRIGGER user_group_user_revoke_user_group_role BEFORE DELETE
ON base.user_group_user FOR EACH ROW EXECUTE PROCEDURE
base.revoke_user_group_role();
