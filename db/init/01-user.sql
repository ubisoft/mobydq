/*Connect to database*/
\connect mobydq



/*Create table user*/
CREATE TABLE base.user (
    id SERIAL PRIMARY KEY
  , email CITEXT NOT NULL UNIQUE
  , "role" CITEXT NOT NULL DEFAULT 'standard'
  , flag_active BOOLEAN DEFAULT TRUE
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id()
  , updated_by_id INTEGER DEFAULT base.get_current_user_id()
);

COMMENT ON TABLE base.user IS
'Users information.';



/*Add circular reference to user table*/
ALTER TABLE base.user ADD CONSTRAINT user_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES base.user(id);
ALTER TABLE base.user ADD CONSTRAINT user_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES base.user(id);



/*Create function to search users*/
CREATE OR REPLACE FUNCTION base.search_user(search_keyword TEXT, sort_attribute TEXT, sort_order TEXT)
RETURNS SETOF base.user AS $$
BEGIN
    RETURN QUERY
    EXECUTE format(
        'SELECT a.*
        FROM base.user a
        WHERE a.email ILIKE (''%%%s%%'') OR a.role ILIKE (''%%%s%%'')
        ORDER BY a.%I %s',
        search_keyword,
        search_keyword,
        sort_attribute,
        sort_order);
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.search_user IS
'Function used to search users based on keywords contained in their email.';



/*Create default user*/
/*Admin user is required to be able to create the default user group later*/
/*Must be created before other triggers to avoid conflicts*/
INSERT INTO base.user (email, role) VALUES ('admin', 'admin');
CREATE ROLE user_1 WITH CREATEROLE;



/*Create function to create database user in pg_roles table when user is created in user table*/
CREATE OR REPLACE FUNCTION base.create_user()
RETURNS TRIGGER AS $$
BEGIN
    -- Create database user
    EXECUTE 'CREATE ROLE user_' || NEW.id || ' WITH CREATEROLE';

    -- Grant permission
    EXECUTE 'GRANT ' || NEW.role || ' TO user_' || NEW.id;

    -- Assign default user group
    INSERT INTO base.user_group_membership (user_id) VALUES (NEW.id);
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.create_user IS
'Function used to automatically create a database user in pg_roles tables when user is created in user table.';



/*Create function to update user permissions in pg_roles table*/
CREATE OR REPLACE FUNCTION base.update_user_permission()
RETURNS TRIGGER AS $$
BEGIN
    -- Update permission
    IF OLD.role <> NEW.role THEN
        -- Revoke permission
        EXECUTE 'REVOKE ' || OLD.role || ' FROM user_' || OLD.id;

        -- Grant permission
        EXECUTE 'GRANT ' || NEW.role || ' TO user_' || NEW.id;
    END IF;
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.update_user_permission IS
'Function used to automatically update permissions of a user in pg_roles table.';



/*Triggers on insert*/
CREATE TRIGGER user_create_user AFTER INSERT
ON base.user FOR EACH ROW EXECUTE PROCEDURE
base.create_user();



/*Triggers on update*/
CREATE TRIGGER user_update_updated_date BEFORE UPDATE
ON base.user FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER user_update_updated_by_id BEFORE UPDATE
ON base.user FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();

CREATE TRIGGER user_update_user_permission BEFORE UPDATE
ON base.user FOR EACH ROW EXECUTE PROCEDURE
base.update_user_permission();
