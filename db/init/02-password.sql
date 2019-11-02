/*Connect to database*/
\connect mobydq



/*Create table password*/
CREATE TABLE base.password (
    id SERIAL PRIMARY KEY
  , "password" TEXT NOT NULL
  , user_id INTEGER NOT NULL UNIQUE REFERENCES base.sys_user(id)
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.sys_user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.sys_user(id)
);

COMMENT ON TABLE base.sys_password IS
'Users password information.';



/*Create function to hash password column*/
CREATE OR REPLACE FUNCTION base.hash_password()
RETURNS TRIGGER AS $$
BEGIN
    NEW.password = crypt(NEW.password, gen_salt('bf', 8));
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.hash_password IS
'Function used to hash password when creating a user.';



/*Create composite type to generate JWT*/
CREATE TYPE base.token AS (
    email TEXT,
    role TEXT,
    aud TEXT  --audience
);

/*Create function to authenticate users*/
CREATE OR REPLACE FUNCTION base.authenticate_user(user_email TEXT, user_password TEXT)
RETURNS base.sys_token AS $$
DECLARE
    user_account RECORD;
BEGIN
    SELECT a.id, a.email, b.password
    INTO user_account
    FROM base.user a
    INNER JOIN base.password b on a.id=b.user_id
    WHERE a.email = user_email
    AND flag_active = true;

    IF user_account.password = crypt(user_password, user_account.password) THEN
        RETURN (
            user_account.email,  --email
            'user_' || user_account.id,  --role
            'postgraphile'  --audience
        )::base.token;
    ELSE
        RETURN NULL;
    END IF;
END;
$$ language plpgsql strict security definer;

COMMENT ON FUNCTION base.authenticate_user IS
'Function used to authenticate users.';



/*Triggers on insert*/
CREATE TRIGGER password_create_hash_password BEFORE INSERT
ON base.password FOR EACH ROW EXECUTE PROCEDURE
base.hash_password();



/*Triggers on update*/
CREATE TRIGGER password_update_hash_password BEFORE UPDATE
ON base.password FOR EACH ROW EXECUTE PROCEDURE
base.hash_password();

CREATE TRIGGER password_update_updated_date BEFORE UPDATE
ON base.password FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER password_update_updated_by_id BEFORE UPDATE
ON base.password FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();



/*Create default user password*/
INSERT INTO base.password (password, user_id) VALUES ('admin', 1);