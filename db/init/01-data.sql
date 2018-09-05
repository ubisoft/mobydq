/*Connect to database*/
\connect data_quality



INSERT INTO base.data_source_type (name) VALUES
('Hive'),
('Impala'),
('MariaDB'),
('Microsoft SQL Server'),
('MySQL'),
('Oracle'),
('PostgreSQL'),
('SQLite'),
('Teradata');



INSERT INTO base.indicator_type (name, module, class, method) VALUES
('Completeness', 'completeness', 'Completeness', 'execute'),
('Freshness', 'freshness', 'Freshness', 'execute'),
('Latency', 'latency', 'Latency', 'execute'),
('Validity', 'validity', 'Validity', 'execute');



INSERT INTO base.parameter_type (name, description) VALUES
('Alert operator', 'Operator used to compare the results of the indicator with the alert threshold. Example: ==, >, >=, <, <=, <>'),
('Alert threshold', 'Numeric value used to evaluate the results of the indicator and determine if an alert must be sent.'),
('Distribution list', 'List of e-mail addresses to which alerts must be sent. Example: [''email_1'', ''email_2'', ''email_3'']'),
('Dimension', 'List of values to indicate dimensions in the results of the indicator. Example: [''dimension_1'', ''dimension_2'', ''dimension_3'']'),
('Measure', 'List of values to indicate measures in the results of the indicator. Example: [''measure_1'', ''measure_2'', ''measure_3'']'),
('Source', 'Name of the data source which serves as a reference to evaluate the quality of the data.'),
('Source request', 'SQL query used to compute the indicator on the source system.'),
('Target', 'Name of the data source on which to evaluate the quality of the data.'),
('Target request', 'SQL query used to compute the indicator on the target system.');
