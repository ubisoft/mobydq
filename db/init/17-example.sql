/*Connect to database*/
\connect mobydq



/*Create data source*/
INSERT INTO base.data_source (name, connection_string, login, password, data_source_type_id, user_group_id) VALUES
(
   'example_cloudera_hive'
  ,'driver={Cloudera Hive};host=db-cloudera;port=10000;'
  ,'cloudera'
  ,'cloudera'
  ,1  -- Cloudera Hive
  ,1  -- Public user group
),
(
   'example_mariadb'
  ,'driver={MariaDB Unicode};server=db-mariadb;port=3306;database=star_wars;'
  ,'root'
  ,'1234'
  ,3  -- MariaDB
  ,1  -- Public user group
),
(
   'example_microsoft_sql_server'
  ,'driver={FreeTDS};server=db-sql-server;port=1433;database=star_wars;tds_version=8.0;'
  ,'sa'
  ,'1234-abcd'
  ,4  -- Microsoft SQL Server
  ,1  -- Public user group
),
(
   'example_mysql'
  ,'driver={MySQL Unicode};server=db-mysql;port=3306;database=star_wars;'
  ,'root'
  ,'1234'
  ,5  -- MySQL
  ,1  -- Public user group
),
(
   'example_oracle'
  ,'driver={Oracle};dbq=db-oracle:1521/orclcdb;'
  ,'oracle'
  ,'1234-abcd'
  ,6  -- Oracle
  ,1  -- Public user group
),
(
   'example_postgresql'
  ,'driver={PostgreSQL Unicode};server=db-postgresql;port=5432;database=star_wars;'
  ,'postgres'
  ,'1234'
  ,7  -- PostgreSQL
  ,1  -- Public user group
)
,(
   'example_snowflake'
  ,'driver={Snowflake};server=account-name.snowflakecomputing.com;port=443;'
  ,'snowflake_user'
  ,'snowflake_password'
  ,10  -- Snowflake
  ,1  -- Public user group
)
,(
   'example_teradata'
  ,'driver={Teradata 64};dbcname=db-teradata;defaultdatabase=star_wars;charset=utf8;'
  ,'dbc'
  ,'1234'
  ,9  -- Teradata
  ,1  -- Public user group
);


/*Create indicator group*/
INSERT INTO base.indicator_group (name, user_group_id) VALUES
(
   'example_indicator_group'
  ,1  -- Public user group
);


/*Create indicators*/
INSERT INTO base.indicator (name, description, execution_order, flag_active, indicator_type_id, indicator_group_id, user_group_id) VALUES
(
   'example_completeness_indicator'
  ,'Example of completeness indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=1)  -- Completeness
  ,(SELECT id FROM base.indicator_group WHERE name='example_indicator_group')
  ,1  -- Public user group
),
(
   'example_freshness_indicator'
  ,'Example of freshness indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=2)  -- Freshness
  ,(SELECT id FROM base.indicator_group WHERE name='example_indicator_group')
  ,1  -- Public user group
),
(
   'example_latency_indicator'
  ,'Example of latency indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=3)  -- Latency
  ,(SELECT id FROM base.indicator_group WHERE name='example_indicator_group')
  ,1  -- Public user group
),
(
   'example_validity_indicator'
  ,'Example of validity indicator'
  ,1
  ,true
  ,(SELECT id FROM base.indicator_type WHERE id=4)  -- Validity
  ,(SELECT id FROM base.indicator_group WHERE name='example_indicator_group')
  ,1  -- Public user group
);


/*Create completeness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'>='
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'0'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''contact.mobydq@gmail.com'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''gender'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''nb_people'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=6)  -- Source
  ,'example_postgresql'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=7)  -- Source request
  ,'SELECT gender, COUNT(id) FROM people GROUP BY gender;'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'example_mysql'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_completeness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT gender, COUNT(id) FROM people GROUP BY gender;'
  ,1  -- Public user group
);


/*Create freshness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'>='
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'0'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''contact.mobydq@gmail.com'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''name'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''last_updated_date'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'example_mysql'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_freshness_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'
  ,1  -- Public user group
);


/*Create latency indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'>='
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'0'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''contact.mobydq@gmail.com'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''name'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''last_updated_date'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=6)  -- Source
  ,'example_postgresql'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=7)  -- Source request
  ,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'example_mysql'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_latency_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'
  ,1  -- Public user group
);


/*Create validity indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value, user_group_id) VALUES
(
   (SELECT id FROM base.indicator WHERE name='example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
  ,'<'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
  ,'1000000'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
  ,'[''contact.mobydq@gmail.com'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
  ,'[''name'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
  ,'[''population'']'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
  ,'example_postgresql'
  ,1  -- Public user group
),
(
   (SELECT id FROM base.indicator WHERE name='example_validity_indicator')
  ,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
  ,'SELECT name, SUM(population) FROM planet WHERE climate=''temperate'' GROUP BY name;'
  ,1  -- Public user group
);
