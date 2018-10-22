/*Connect to database*/
\connect mobydq



/*Create table indicator group*/
CREATE TABLE base.indicator_group (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , user_group TEXT NOT NULL
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE base.indicator_group IS
'Indicator groups define collections of indicators to be computed in the same batch.';

CREATE TRIGGER indicator_group_updated_date BEFORE UPDATE
ON base.indicator_group FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

CREATE TRIGGER indicator_group_delete_indicator BEFORE DELETE
ON base.indicator_group FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('indicator', 'indicator_group_id');
