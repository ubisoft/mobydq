/*Create database*/
CREATE DATABASE data_quality;
\connect data_quality;


/*Create schema*/
CREATE SCHEMA base;


/*Create function to update updated_date column*/
CREATE OR REPLACE FUNCTION base.update_updated_date_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_date = now();
   RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.update_updated_date_column IS
'Function used to automatically update the updated_date column in tables.';


/*Create table data source type*/
CREATE TABLE base.data_source_type (
    id SERIAL PRIMARY KEY,
    data_source_type TEXT NOT NULL UNIQUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE base.data_source_type IS
'Data source types describe the types of a data sources the data quality framework can connect to.';

CREATE TRIGGER data_source_type_updated_date BEFORE UPDATE
ON base.data_source_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

INSERT INTO base.data_source_type (data_source_type) VALUES
('Hive'),
('Impala'),
('Microsoft SQL Server'),
('MySQL'),
('PostgreSQL'),
('SQLite'),
('Teradata');


/*Create table data source*/
CREATE TABLE base.data_source (
    id SERIAL PRIMARY KEY,
    data_source TEXT NOT NULL UNIQUE,
    connection_string TEXT,
    login TEXT,
    password TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source_type_id INTEGER NOT NULL REFERENCES base.data_source_type(id)
);

COMMENT ON TABLE base.data_source IS
'Data sources are systems containing or exposing data on which the data quality framework can compute indicators.';

CREATE TRIGGER data_source_updated_date BEFORE UPDATE
ON base.data_source FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();


/*Create table indicator type*/
CREATE TABLE base.indicator_type (
    id SERIAL PRIMARY KEY,
    indicator_type TEXT NOT NULL UNIQUE,
    function TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE base.indicator_type IS
'Indicator types determine which function of the data quality framework is used to compute indicators.';

CREATE TRIGGER indicator_type_updated_date BEFORE UPDATE
ON base.indicator_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

INSERT INTO base.indicator_type (indicator_type, function) VALUES
('Completeness', 'evaluate_completeness'),
('Freshness', 'evaluate_freshness'),
('Latency', 'evaluate_latency'),
('Validity', 'evaluate_validity');


/*Create table indicator group*/
CREATE TABLE base.indicator_group (
    id SERIAL PRIMARY KEY,
    indicator_group TEXT NOT NULL UNIQUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE base.indicator_group IS
'Indicator groups define collections of indicators to be computed in the same batch.';

CREATE TRIGGER indicator_group_updated_date BEFORE UPDATE
ON base.indicator_group FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();


/*Create table indicator*/
CREATE TABLE base.indicator (
    id SERIAL PRIMARY KEY,
    indicator TEXT NOT NULL UNIQUE,
    description TEXT,
    execution_order INTEGER DEFAULT 0,
    flag_active BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    indicator_type_id INTEGER NOT NULL REFERENCES base.indicator_type(id),
    indicator_group_id INTEGER NOT NULL REFERENCES base.indicator_group(id)
);

COMMENT ON TABLE base.indicator IS
'Indicators compute data sets on one or several data sources in order to evaluate the quality of their data.';

CREATE TRIGGER indicator_updated_date BEFORE UPDATE
ON base.indicator FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();


/*Create table parameter type*/
CREATE TABLE base.parameter_type (
    id SERIAL PRIMARY KEY,
    parameter_type TEXT NOT NULL UNIQUE,
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE base.parameter_type IS
'Parameter types determine which types of parameters can be used to compute indicators.';

CREATE TRIGGER parameter_type_updated_date BEFORE UPDATE
ON base.parameter_type FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();

INSERT INTO base.parameter_type (parameter_type, description) VALUES
('Alert operator', 'Operator used to compare the results of the indicator with the alert threshold. Example: =, >, >=, <, <=, <>'),
('Alert threshold', 'Numeric value used to evaluate the results of the indicator and determine if an alert must be sent.'),
('Distribution list', 'List of e-mail addresses to which alerts must be sent. Example: [''email_1'', ''email_2'', ''email_3'']'),
('Dimension', 'List of values to indicate dimensions in the results of the indicator. Example: [''dimension_1'', ''dimension_2'', ''dimension_3'']'),
('Measure', 'List of values to indicate measures in the results of the indicator. Example: [''measure_1'', ''measure_2'', ''measure_3'']'),
('Source', 'Name of the data source which serves as a reference to evaluate the quality of the data.'),
('Source request', 'SQL query used to compute the indicator on the source system.'),
('Target', 'Name of the data source on which to evaluate the quality of the data.'),
('Target request', 'SQL query used to compute the indicator on the target system.');


/*Create table parameter*/
CREATE TABLE base.parameter (
    id SERIAL PRIMARY KEY,
    value TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parameter_type_id INTEGER NOT NULL REFERENCES base.parameter_type(id),
    indicator_id INTEGER NOT NULL REFERENCES base.indicator(id)
);

COMMENT ON TABLE base.parameter IS
'Parameters used by the data quality framework to compute indicators.';

CREATE TRIGGER parameter_updated_date BEFORE UPDATE
ON base.parameter FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();


/*Create table batch*/
CREATE TABLE base.batch (
    id SERIAL PRIMARY KEY,
    status TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    indicator_group_id INTEGER NOT NULL REFERENCES base.indicator_group(id)
);

COMMENT ON TABLE base.batch IS
'Batches record the execution of groups of indicators.';

CREATE TRIGGER batch_updated_date BEFORE UPDATE
ON base.batch FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();


/*Create table session*/
CREATE TABLE base.session (
    id SERIAL PRIMARY KEY,
    status TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    batch_id INTEGER NOT NULL REFERENCES base.batch(id),
    indicator_id INTEGER NOT NULL REFERENCES base.indicator(id)
);

COMMENT ON TABLE base.session IS
'Sessions record the execution of indicators within a batch.';

CREATE TRIGGER session_updated_date BEFORE UPDATE
ON base.session FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date_column();


/*Create table indicator result*/
CREATE TABLE base.indicator_result (
    id SERIAL PRIMARY KEY,
    alert_operator TEXT NOT NULL,
    alert_threshold FLOAT NOT NULL,
    nb_records INTEGER NOT NULL,
    nb_records_alert INTEGER NOT NULL,
    nb_records_no_alert INTEGER NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id INTEGER NOT NULL REFERENCES base.session(id),
    indicator_id INTEGER NOT NULL REFERENCES base.indicator(id)
);

COMMENT ON TABLE base.indicator_result IS
'Indicator results contain a summary of indicators execution.';


/*Create function to execute indicator group*/
CREATE OR REPLACE FUNCTION base.execute_indicator_group(indicator_group_id INTEGER, indicator_id INTEGER ARRAY DEFAULT NULL)
RETURNS base.batch AS $$
#variable_conflict use_variable
DECLARE
    batch base.batch;
BEGIN
    -- Create pending batch
    INSERT INTO base.batch (status, indicator_group_id)
    VALUES ('Pending', indicator_group_id)
    RETURNING * INTO batch;

    -- Create pending session for each indicator
    IF indicator_id IS NOT NULL THEN
        WITH indicator AS (
            SELECT a.id
            FROM base.indicator a
            WHERE a.indicator_group_id=indicator_group_id
            AND a.id=ANY(indicator_id)
            ORDER BY a.execution_order
        ) INSERT INTO base.session (status, indicator_id, batch_id)
        SELECT 'Pending', indicator.id, batch.id FROM indicator;
    ELSE
        WITH indicator AS (
            SELECT a.id
            FROM base.indicator a
            WHERE a.indicator_group_id=indicator_group_id
            ORDER BY a.execution_order
        ) INSERT INTO base.session (status, indicator_id, batch_id)
        SELECT 'Pending', indicator.id, batch.id FROM indicator;
    END IF;

    -- Trigger execution of indicators
    COPY batch.id TO PROGRAM 'echo "Hello World!"';

    -- Return batch record
    RETURN batch;
END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;

COMMENT ON FUNCTION base.execute_indicator_group IS
'Function used to execute a group of indicators.';
