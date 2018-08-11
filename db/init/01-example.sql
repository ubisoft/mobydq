/*Connect to database*/
\connect data_quality


/*Create data source*/
INSERT INTO base.data_source (name, connection_string, login, password, data_source_type_id) VALUES
('dq_example_mysql'
,'driver={MySQL ODBC 3.51 Driver};server=0.0.0.0;port=9000;database=star_wars;'
,'root'
,'1234'
,(SELECT id FROM base.data_source_type WHERE name='MySQL')),
('dq_example_postgresql'
,'driver={PostgreSQL Unicode};server=0.0.0.0;port=9001;database=star_wars;'
,'postgres'
,'1234'
,(SELECT id FROM base.data_source_type WHERE name='PostgreSQL'));


/*Create indicator group*/
INSERT INTO base.indicator_group (name) VALUES
('dq_example_indicator_group');


/*Create indicators*/
INSERT INTO base.indicator (name, description, execution_order, flag_active, indicator_type_id, indicator_group_id) VALUES
('dq_example_completeness_indicator'
,'Example of completeness indicator'
,1
,true
,(SELECT id FROM base.indicator_type WHERE name='Completeness')
,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')),
('dq_example_freshness_indicator'
,'Example of freshness indicator'
,1
,true
,(SELECT id FROM base.indicator_type WHERE name='Freshness')
,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')),
('dq_example_latency_indicator'
,'Example of latency indicator'
,1
,true
,(SELECT id FROM base.indicator_type WHERE name='Latency')
,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group')),
('dq_example_validity_indicator'
,'Example of validity indicator'
,1
,true
,(SELECT id FROM base.indicator_type WHERE name='Validity')
,(SELECT id FROM base.indicator_group WHERE name='dq_example_indicator_group'));


/*Create completeness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value) VALUES
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Alert operator')
,'>='),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Alert threshold')
,'0'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Distribution list')
,'change.me@example.com'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Dimension')
,'[''gender'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Measure')
,'[''nb_people'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Source')
,'dq_example_postgresql'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Source request')
,'SELECT gender, COUNT(id) FROM people GROUP BY gender;'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Target')
,'dq_example_mysql'),
((SELECT id FROM base.indicator WHERE name='dq_example_completeness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Target request')
,'SELECT gender, COUNT(id) FROM people GROUP BY gender;');


/*Create freshness indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value) VALUES
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Alert operator')
,'>='),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Alert threshold')
,'0'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Distribution list')
,'change.me@example.com'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Dimension')
,'[''name'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Measure')
,'[''last_updated_date'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Target')
,'dq_example_postgresql'),
((SELECT id FROM base.indicator WHERE name='dq_example_freshness_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Target request')
,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;');


/*Create latency indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value) VALUES
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Alert operator')
,'>='),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Alert threshold')
,'0'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Distribution list')
,'change.me@example.com'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Dimension')
,'[''name'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Measure')
,'[''last_updated_date'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Source')
,'dq_example_postgresql'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Source request')
,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Target')
,'dq_example_mysql'),
((SELECT id FROM base.indicator WHERE name='dq_example_latency_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Target request')
,'SELECT name, MAX(updated_date) FROM people WHERE name LIKE ''%Skywalker%'' GROUP BY name;');


/*Create validity indicator parameters*/
INSERT INTO base.parameter (indicator_id, parameter_type_id, value) VALUES
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Alert operator')
,'<'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Alert threshold')
,'1000000'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Distribution list')
,'change.me@example.com'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Dimension')
,'[''name'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Measure')
,'[''population'']'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Target')
,'dq_example_postgresql'),
((SELECT id FROM base.indicator WHERE name='dq_example_validity_indicator')
,(SELECT id FROM base.parameter_type WHERE name='Target request')
,'SELECT name, population FROM planet WHERE terrain=''temperate'' GROUP BY name;');
