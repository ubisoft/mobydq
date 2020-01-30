/*Connect to database*/
\connect mobydq



/*Create table log*/
CREATE TABLE base.log (
    id SERIAL PRIMARY KEY
  , file_name TEXT
  , log_level TEXT
  , message TEXT
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , batch_id INTEGER REFERENCES base.batch(id)
  , session_id INTEGER REFERENCES base.session(id)
  , data_source_id INTEGER REFERENCES base.data_source(id)
);

COMMENT ON TABLE base.log IS
'Logs recorded during the execution of batches, sessions and tests of data sources.';

CREATE TRIGGER batch_delete_log BEFORE DELETE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('log', 'batch_id');

CREATE TRIGGER session_delete_log BEFORE DELETE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('log', 'session_id');

CREATE TRIGGER data_source_delete_log BEFORE DELETE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('log', 'data_source_id');



/*Create function to search logs*/
CREATE OR REPLACE FUNCTION base.search_log(search_keyword TEXT, sort_attribute TEXT, sort_order TEXT)
RETURNS SETOF base.log AS $$
BEGIN
    RETURN QUERY
    EXECUTE format(
        'SELECT a.*
        FROM base.log a
        WHERE a.file_name ILIKE (''%%%s%%'') OR a.log_level ILIKE (''%%%s%%'') OR a.message ILIKE (''%%%s%%'')
        ORDER BY a.%I %s',
        search_keyword,
        sort_attribute,
        sort_order);
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.search_log IS
'Function used to search logs based on keywords contained in the file name, log level or message.';