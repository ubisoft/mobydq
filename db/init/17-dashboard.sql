/*Connect to database*/
\connect mobydq



/*Create view to get batch status summary*/
CREATE OR REPLACE VIEW base.batch_status
AS SELECT a.id
  , a.status
  , a.created_date
  , a.updated_date
  , (DATE_PART('day', a.updated_date::timestamp - a.created_date::timestamp)*24 +
     DATE_PART('hour', a.updated_date::timestamp - a.created_date::timestamp))*60 +
     DATE_PART('minute', a.updated_date::timestamp - a.created_date::timestamp) as duration_minutes
  , a.updated_date::timestamp - a.created_date::timestamp as duration
  , a.user_group_id
  , b.name as indicator_group_name
  , COUNT(DISTINCT c.id) as nb_sessions
FROM base.batch a
INNER JOIN base.indicator_group b ON a.indicator_group_id=b.id
INNER JOIN base.session c ON a.id=c.batch_id
GROUP BY a.id
  , b.name;

COMMENT ON VIEW base.batch_status IS
'View used to to get batch status summary.';



/*Create view to get batch statistics*/
CREATE OR REPLACE VIEW base.batch_statistics
AS SELECT created_date::date as "date"
  , COUNT(DISTINCT id) as nb_batches
  , SUM(duration_minutes) as sum_duration_minutes
  , SUM(duration) as sum_duration
FROM base.batch_status
GROUP BY created_date::date;

COMMENT ON VIEW base.batch_statistics IS
'View used to to get batch statistics.';



/*Create view to get session status summary*/
CREATE OR REPLACE VIEW base.session_status
AS SELECT a.id
  , a.status
  , a.created_date
  , a.updated_date
  , (DATE_PART('day', a.updated_date::timestamp - a.created_date::timestamp)*24 +
     DATE_PART('hour', a.updated_date::timestamp - a.created_date::timestamp))*60 +
     DATE_PART('minute', a.updated_date::timestamp - a.created_date::timestamp) as duration_minutes
  , a.updated_date::timestamp - a.created_date::timestamp as duration
  , a.user_group_id
  , a.id as batch_id
  , c.name as indicator_group_name
FROM base.session a
INNER JOIN base.batch b ON a.batch_id=b.id
INNER JOIN base.indicator_group c ON b.indicator_group_id=c.id;

COMMENT ON VIEW base.session_status IS
'View used to to get session status summary.';



/*Create view to get session statistics*/
CREATE OR REPLACE VIEW base.session_statistics
AS SELECT created_date::date as "date"
  , COUNT(DISTINCT id) as nb_sessions
  , SUM(duration_minutes) as sum_duration_minutes
  , SUM(duration) as sum_duration
FROM base.session_status
GROUP BY created_date::date;

COMMENT ON VIEW base.session_statistics IS
'View used to to get session statistics.';
