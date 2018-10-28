/*Connect to database*/
\connect mobydq



/*Create table user group*/
CREATE TABLE base.user_group_user (
    id SERIAL PRIMARY KEY
  , user_group_id INTEGER NOT NULL REFERENCES base.user_group(id)
  , user_id INTEGER NOT NULL REFERENCES base.user(id)
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , CONSTRAINT user_group_user_uniqueness UNIQUE (user_group_id, user_id)
);

COMMENT ON TABLE base.user_group IS
'User groups users show which groups users are members of.';



/*Create function to grant user group role to user*/
CREATE OR REPLACE FUNCTION base.grant_user_group()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE 'GRANT user_group_' || NEW.user_group_id || ' TO user_' || NEW.user_id;
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.create_user_group IS
'Function used to automatically grant a user group to a user.';

CREATE TRIGGER user_group_user_grant_user_group AFTER INSERT
ON base.user_group_user FOR EACH ROW EXECUTE PROCEDURE
base.grant_user_group();



/*Create function to revoke user group role to user*/
CREATE OR REPLACE FUNCTION base.revoke_user_group()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE 'REVOKE user_group_' || OLD.user_group_id || ' FROM user_' || OLD.user_id;
    RETURN OLD;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.revoke_user_group IS
'Function used to automatically revoke a user group from a user.';

CREATE TRIGGER user_group_user_revoke_user_group BEFORE DELETE
ON base.user_group_user FOR EACH ROW EXECUTE PROCEDURE
base.revoke_user_group();
