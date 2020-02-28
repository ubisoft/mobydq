/*Connect to database*/
\connect mobydq



/*Create table indicator group*/
CREATE TABLE base.indicator_group (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , user_group_id INTEGER DEFAULT 1 REFERENCES base.user_group(id)
);

COMMENT ON TABLE base.indicator_group IS
'Indicator groups define collections of indicators to be computed in the same batch.';



/*Triggers on update*/
CREATE TRIGGER indicator_group_update_updated_date BEFORE UPDATE
ON base.indicator_group FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER indicator_group_update_updated_by_id BEFORE UPDATE
ON base.indicator_group FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();



/*Triggers on delete*/
CREATE TRIGGER indicator_group_delete_indicator BEFORE DELETE
ON base.indicator_group FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('indicator', 'indicator_group_id');

CREATE TRIGGER indicator_group_delete_batch BEFORE DELETE
ON base.indicator_group FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('batch', 'indicator_group_id');



/*Create function to search indicator groups*/
CREATE OR REPLACE FUNCTION base.search_indicator_group(search_keyword TEXT, sort_attribute TEXT, sort_order TEXT)
RETURNS SETOF base.indicator_group AS $$
BEGIN
    RETURN QUERY
    EXECUTE format(
        'SELECT a.*
        FROM base.indicator_group a
        WHERE a.name ILIKE (''%%%s%%'')
        ORDER BY a.%I %s',
        search_keyword,
        sort_attribute,
        sort_order);
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.search_indicator_group IS
'Function used to search indicator groups based on keywords contained in their name.';