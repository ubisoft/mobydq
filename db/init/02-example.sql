/*Connect to database*/
\connect mobydq


/*Create data source*/
INSERT INTO base.data_source (name, connection_string, login, password, data_source_type_id) VALUES
(
  'dq_example_microsoft_sql_server'
  ,'driver={FreeTDS};server=10.0.2.15;port=9000;database=star_wars;tds_version=8.0;'
  ,'sa'
  ,'1234-abcd'
  ,4  -- Microsoft SQL Server
)
,(
  'dq_example_mysql'
  ,'driver={MySQL Unicode};server=10.0.2.15;port=9001;database=star_wars;'
  ,'root'
  ,'1234'
  ,5  -- MySQL
)
,(
  'dq_example_postgresql'
  ,'driver={PostgreSQL Unicode};server=10.0.2.15;port=9002;database=star_wars;'
  ,'postgres'
  ,'1234'
  ,7  -- PostgreSQL
)
,(
  'dq_example_teradata'
  ,'driver={Teradata 64};dbcname=10.0.2.15;defaultdatabase=star_wars;charset=utf8;'
  ,'dbc'
  ,'1234'
  ,9  -- Teradata
);


/*Create indicator group*/
INSERT INTO base.indicator_group (name) VALUES
('dq_example_indicator_group');


/*Create indicators*/
INSERT INTO base.indicator (name, description, execution_order, flag_active, indicator_type_id, indicator_group_id) VALUES
('dq_example_completeness_indicator'
,'Example of completeness indicator'
,1
,true
,(SELECT id FROM base.indicator_type WHERE id=1)  -- Completeness
,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')),
('dq_example_freshness_indicator'
,'Example of freshness indicator'
,1
,true
,(SELECT id FROM base.indicator_type WHERE id=2)  -- Freshness
,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')),
('dq_example_latency_indicator'
,'Example of latency indicator'
,1
,true
,(SELECT id FROM base.indicator_type WHERE id=3)  -- Latency
,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')),
('dq_example_validity_indicator'
,'Example of validity indicator'
,1
,true
,(SELECT id FROM base.indicator_type WHERE id=4)  -- Validity
,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group'));


/*Create completeness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value) VALUES
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
,'>='),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
,'0'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
,'[''change.me@example.com'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
,'[''gender'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
,'[''nb_people'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=6)  -- Source
,'dq_example_postgresql'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=7)  -- Source request
,'SELECT gender, COUNT(id) FROM people GROUP BY gender;'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
,'dq_example_microsoft_sql_server'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
,'SELECT gender, COUNT(id) FROM dbo.people GROUP BY gender;');


/*Create freshness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value) VALUES
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
,'>='),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
,'0'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
,'[''change.me@example.com'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
,'[''name'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
,'[''last_updated_date'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
,'dq_example_mysql'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;');


/*Create latency indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value) VALUES
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
,'>='),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
,'0'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
,'[''change.me@example.com'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
,'[''name'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
,'[''last_updated_date'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE id=6)  -- Source
,'dq_example_postgresql'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE id=7)  -- Source request
,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
,'dq_example_microsoft_sql_server'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
,'SELECT name, MAX(updated_date) FROM dbo.people WHERE name LIKE ''%Skywalker%'' GROUP BY name;');


/*Create validity indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value) VALUES
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE id=1)  -- Alert operator
,'<'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE id=2)  -- Alert threshold
,'1000000'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE id=3)  -- Distribution list
,'[''change.me@example.com'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE id=4)  -- Dimension
,'[''name'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE id=5)  -- Measure
,'[''population'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE id=8)  -- Target
,'dq_example_postgresql'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE id=9)  -- Target request
,'SELECT name, SUM(population) FROM planet WHERE climate=''temperate'' GROUP BY name;');
