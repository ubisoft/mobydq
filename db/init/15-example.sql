/*Connect to database*/
\connect mobydq



/*Create user group*/
INSERT INTO base.user_group (name) VALUES ('user_group_example');

/*Create user*/
INSERT INTO base.user (email, oauth_type, access_token, expiry_date) VALUES
('user@example.com', 'GOOGLE', '1234', '2999-12-31');

/*Assign group to user*/
DO $$
DECLARE
  user_id TEXT;
  user_group_id TEXT;
BEGIN
  SELECT id INTO user_id FROM base.user WHERE email='user@example.com';
  SELECT id INTO user_group_id FROM base.user_group WHERE name='user_group_example';
  EXECUTE 'GRANT user_group_' || user_group_id || ' TO user_' || user_id;
END;
$$;



/*Create data source*/
INSERT INTO base.data_source (name, connection_string, login, password, data_source_type_id, user_group_id) VALUES
(
   'dq_example_microsoft_sql_server'
  ,'driver={FreeTDS};server=db-sql-server;port=1433;database=star_wars;tds_version=8.0;'
  ,'sa'
  ,'1234-abcd'
  ,4  -- Microsoft SQL Server
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
)
,(
   'dq_example_mysql'
  ,'driver={MySQL Unicode};server=db-mysql;port=3306;database=star_wars;'
  ,'root'
  ,'1234'
  ,5  -- MySQL
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
)
,(
   'dq_example_postgresql'
  ,'driver={PostgreSQL Unicode};server=db-postgresql;port=5432;database=star_wars;'
  ,'postgres'
  ,'1234'
  ,7  -- PostgreSQL
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
)
,(
   'dq_example_teradata'
  ,'driver={Teradata 64};dbcname=db-teradata;defaultdatabase=star_wars;charset=utf8;'
  ,'dbc'
  ,'1234'
  ,9  -- Teradata
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
);


/*Create indicator group*/
INSERT INTO base.indicator_group (name, user_group_id) VALUES
(
   'dq_example_indicator_group'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
);


/*Create indicators*/
INSERT INTO base.indicator (name, description, execution_order, flag_active, indicator_type_id, indicator_group_id, user_group_id) VALUES
(
   'dq_example_completeness_indicator'
  ,'Example of completeness indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=1)  -- Completeness
  ,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   'dq_example_freshness_indicator'
  ,'Example of freshness indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=2)  -- Freshness
  ,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   'dq_example_latency_indicator'
  ,'Example of latency indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=3)  -- Latency
  ,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   'dq_example_validity_indicator'
  ,'Example of validity indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=4)  -- Validity
  ,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
);


/*Create completeness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'>='
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'0'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''change.me@example.com'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''gender'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''nb_people'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=6)  -- Source
  ,'dq_example_postgresql'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=7)  -- Source request
  ,'SELECT gender, COUNT(id) FROM people GROUP BY gender;'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'dq_example_microsoft_sql_server'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT gender, COUNT(id) FROM dbo.people GROUP BY gender;'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
);


/*Create freshness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'>='
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'0'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''change.me@example.com'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''name'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''last_updated_date'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'dq_example_mysql'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
);


/*Create latency indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'>='
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'0'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''change.me@example.com'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''name'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''last_updated_date'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=6)  -- Source
  ,'dq_example_postgresql'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=7)  -- Source request
  ,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'dq_example_microsoft_sql_server'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT name, MAX(updated_date) FROM dbo.people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
);


/*Create validity indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'<'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'1000000'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''change.me@example.com'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''name'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''population'']'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'dq_example_postgresql'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT name, SUM(population) FROM planet WHERE climate=''temperate'' GROUP BY name;'
  ,(SELECT id FROM base.user_group WHERE name='user_group_example')
);
