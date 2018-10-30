/*Connect to database*/
\connect mobydq



/*Create user*/
INSERT INTO base.user (email, oauth_type, access_token, expiry_date) VALUES
('user@example.com', 'GOOGLE', '1234', '2999-12-31');



/*Create data source*/
INSERT INTO base.data_source (name, connection_string, login, password, data_source_type_id, user_group_id) VALUES
(
   'dq_example_microsoft_sql_server'
  ,'driver={FreeTDS};server=db-sql-server;port=1433;database=star_wars;tds_version=8.0;'
  ,'sa'
  ,'1234-abcd'
  ,4  -- Microsoft SQL Server
  ,0  -- Public user group
)
,(
   'dq_example_mysql'
  ,'driver={MySQL Unicode};server=db-mysql;port=3306;database=star_wars;'
  ,'root'
  ,'1234'
  ,5  -- MySQL
  ,0  -- Public user group
)
,(
   'dq_example_postgresql'
  ,'driver={PostgreSQL Unicode};server=db-postgresql;port=5432;database=star_wars;'
  ,'postgres'
  ,'1234'
  ,7  -- PostgreSQL
  ,0  -- Public user group
)
,(
   'dq_example_teradata'
  ,'driver={Teradata 64};dbcname=db-teradata;defaultdatabase=star_wars;charset=utf8;'
  ,'dbc'
  ,'1234'
  ,9  -- Teradata
  ,0  -- Public user group
);


/*Create indicator group*/
INSERT INTO base.indicator_group (name, user_group_id) VALUES
(
   'dq_example_indicator_group'
  ,0  -- Public user group
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
  ,0  -- Public user group
),
(
   'dq_example_freshness_indicator'
  ,'Example of freshness indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=2)  -- Freshness
  ,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')
  ,0  -- Public user group
),
(
   'dq_example_latency_indicator'
  ,'Example of latency indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=3)  -- Latency
  ,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')
  ,0  -- Public user group
),
(
   'dq_example_validity_indicator'
  ,'Example of validity indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=4)  -- Validity
  ,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')
  ,0  -- Public user group
);


/*Create completeness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'>='
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'0'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''change.me@example.com'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''gender'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''nb_people'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=6)  -- Source
  ,'dq_example_postgresql'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=7)  -- Source request
  ,'SELECT gender, COUNT(id) FROM people GROUP BY gender;'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'dq_example_microsoft_sql_server'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT gender, COUNT(id) FROM dbo.people GROUP BY gender;'
  ,0  -- Public user group
);


/*Create freshness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'>='
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'0'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''change.me@example.com'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''name'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''last_updated_date'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'dq_example_mysql'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'
  ,0  -- Public user group
);


/*Create latency indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'>='
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'0'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''change.me@example.com'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''name'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''last_updated_date'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=6)  -- Source
  ,'dq_example_postgresql'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=7)  -- Source request
  ,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'dq_example_microsoft_sql_server'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT name, MAX(updated_date) FROM dbo.people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'
  ,0  -- Public user group
);


/*Create validity indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'<'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'1000000'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''change.me@example.com'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''name'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''population'']'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'dq_example_postgresql'
  ,0  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT name, SUM(population) FROM planet WHERE climate=''temperate'' GROUP BY name;'
  ,0  -- Public user group
);
