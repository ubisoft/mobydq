/*Connect to database*/
\connect mobydq



/*Create table user*/
CREATE TABLE base.user (
    id SERIAL PRIMARY KEY
  , email TEXT NOT NULL UNIQUE
  , oauth_type TEXT NOT NULL
  , access_token TEXT NOT NULL
  , refresh_token INTEGER
  , expiry_date TIMESTAMP NOT NULL
  , flag_admin BOOLEAN DEFAULT FALSE
  , flag_active BOOLEAN DEFAULT TRUE
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE base.user IS
'Users information and their authentication methods.';

CREATE TRIGGER user_updated_date BEFORE UPDATE
ON base.user FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();



/*Create function to create user role*/
CREATE OR REPLACE FUNCTION base.create_user_role()
RETURNS TRIGGER AS $$
DECLARE
    user_role TEXT := 'user_' || NEW.id;
BEGIN
    EXECUTE 'CREATE USER ' || user_role || ' WITH PASSWORD ''' || user_role || '''';

    IF NEW.flag_admin THEN
      EXECUTE 'GRANT admin TO ' || user_role;
    ELSE
      EXECUTE 'GRANT standard TO ' || user_role;
    END IF;
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.create_user_role IS
'Function used to automatically create a user role and assign him permissions.';

CREATE TRIGGER user_create_user_role AFTER INSERT
ON base.user FOR EACH ROW EXECUTE PROCEDURE
base.create_user_role();



/*Create function to update user role*/
CREATE OR REPLACE FUNCTION base.update_user_role()
RETURNS TRIGGER AS $$
DECLARE
    user_role TEXT := 'user_' || NEW.id;
BEGIN
    IF OLD.flag_admin <> NEW.flag_admin THEN
      IF NEW.flag_admin THEN
        EXECUTE 'GRANT admin TO ' || user_role;
        EXECUTE 'REVOKE standard FROM ' || user_role;
      ELSE
        EXECUTE 'GRANT standard TO ' || user_role;
        EXECUTE 'REVOKE admin FROM ' || user_role;
      END IF;
    END IF;
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.update_user_role IS
'Function used to automatically update the permissions of a user.';

CREATE TRIGGER user_update_user_role BEFORE UPDATE
ON base.user FOR EACH ROW EXECUTE PROCEDURE
base.update_user_role();
