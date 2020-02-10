/*Connect to database*/
\connect mobydq



/*Create view number of indicators*/
CREATE OR REPLACE VIEW base.nb_indicators
AS SELECT a.flag_active
  ,b.name AS indicator_type
  ,COUNT(DISTINCT a.id) AS nb_indicators
FROM base.indicator a
INNER JOIN base.indicator_type b ON a.indicator_type_id = b.id
GROUP BY a.flag_active
  ,b.name;

COMMENT ON VIEW base.nb_indicators IS
'View used to get the number of indicators per indicator type and active flag.';



/*Create view to get batch status summary*/
CREATE OR REPLACE VIEW base.batch_status
AS SELECT a.id
  , b.name as indicator_group
  , a.status
  , a.created_date
  , a.updated_date
  , (DATE_PART('day', a.updated_date::timestamp - a.created_date::timestamp)*24 +
     DATE_PART('hour', a.updated_date::timestamp - a.created_date::timestamp))*60 +
     DATE_PART('minute', a.updated_date::timestamp - a.created_date::timestamp) AS duration_minutes
  , a.updated_date::timestamp - a.created_date::timestamp AS duration
  , COUNT(DISTINCT c.id) AS nb_sessions
FROM base.batch a
INNER JOIN base.indicator_group b ON a.indicator_group_id=b.id
INNER JOIN base.session c ON a.id=c.batch_id
GROUP BY a.id
  , b.name;

COMMENT ON VIEW base.batch_status IS
'View used to get batch status summary.';



/*Create view to get batch statistics*/
CREATE OR REPLACE VIEW base.batch_statistics
AS SELECT created_date::date as "date"
  , COUNT(DISTINCT id) as nb_batches
  , SUM(duration_minutes) as sum_duration_minutes
  , SUM(duration) as sum_duration
FROM base.batch_status
GROUP BY created_date::date;

COMMENT ON VIEW base.batch_statistics IS
'View used to get batch statistics.';



/*Create view to get session status summary*/
CREATE OR REPLACE VIEW base.session_status
AS SELECT a.id
  , a.batch_id
  , a.indicator_id
  , b.name AS indicator
  , c.name AS indicator_type
  , a.status
  , a.created_date
  , a.updated_date
  , (DATE_PART('day', a.updated_date::timestamp - a.created_date::timestamp)*24 +
     DATE_PART('hour', a.updated_date::timestamp - a.created_date::timestamp))*60 +
     DATE_PART('minute', a.updated_date::timestamp - a.created_date::timestamp) AS duration_minutes
  , a.updated_date::timestamp - a.created_date::timestamp AS duration
  , CASE WHEN a.nb_records IS NOT NULL
    THEN a.nb_records_no_alert / CAST(a.nb_records AS DECIMAL)
    ELSE 0 END AS quality_level
FROM base.session a
INNER JOIN base.indicator b ON a.indicator_id=b.id
INNER JOIN base.indicator_type c ON b.indicator_type_id=c.id;

COMMENT ON VIEW base.session_status IS
'View used to get session status summary.';



/*Create view to get session statistics*/
CREATE OR REPLACE VIEW base.session_statistics
AS SELECT created_date::date as "date"
  , COUNT(DISTINCT id) as nb_sessions
  , SUM(duration_minutes) as sum_duration_minutes
  , SUM(duration) as sum_duration
FROM base.session_status
GROUP BY created_date::date;

COMMENT ON VIEW base.session_statistics IS
'View used to get session statistics.';
