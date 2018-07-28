CREATE DATABASE data_quality;
\connect data_quality;
CREATE SCHEMA base;


/*Create tables*/
CREATE TABLE base.data_source_type (
    id SERIAL PRIMARY KEY,
    data_source_type TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE base.data_source_type IS
'Data source types describe the types of a data sources the data quality framework can connect to.';


CREATE TABLE base.data_source (
    id SERIAL PRIMARY KEY,
    data_source TEXT NOT NULL,
    connection_string TEXT,
    login TEXT,
    password TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source_type_id INTEGER NOT NULL REFERENCES base.data_source_type(id)
);
COMMENT ON TABLE base.data_source IS
'Data sources are systems containing or exposing data on which the data quality framework can compute indicators.';


CREATE TABLE base.indicator_type (
    id SERIAL PRIMARY KEY,
    indicator_type TEXT NOT NULL,
    function TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE base.indicator_type IS
'Indicator types determine which function of the data quality framework is used to compute indicators.';


CREATE TABLE base.indicator_group (
    id SERIAL PRIMARY KEY,
    indicator_group TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE base.indicator_group IS
'Indicator groups define collections of indicators to be computed in the same batch.';


CREATE TABLE base.indicator (
    id SERIAL PRIMARY KEY,
    indicator TEXT NOT NULL,
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


CREATE TABLE base.parameter_type (
    id SERIAL PRIMARY KEY,
    parameter_type TEXT NOT NULL,
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE base.parameter_type IS
'Parameter types determine which types of parameters can be used to compute indicators.';


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


CREATE TABLE base.batch (
    id SERIAL PRIMARY KEY,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    indicator_group_id INTEGER NOT NULL REFERENCES base.indicator_group(id)
);
COMMENT ON TABLE base.batch IS
'Batches record the execution of groups of indicators.';


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
