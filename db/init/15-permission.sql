/*Connect to database*/
\connect mobydq



/*Create standard user role*/
CREATE ROLE standard;
GRANT USAGE ON SCHEMA base TO standard;
GRANT SELECT, UPDATE, INSERT, DELETE ON base.data_source TO standard;
GRANT SELECT, UPDATE, INSERT, DELETE ON base.indicator_group TO standard;
GRANT SELECT, UPDATE, INSERT, DELETE ON base.indicator TO standard;
GRANT SELECT, UPDATE, INSERT, DELETE ON base.parameter TO standard;



/*Create admin user role*/
CREATE ROLE admin;
GRANT standard TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON base.data_source_type TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON base.indicator_type TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON base.parameter_type TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON base.user TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON base.user_group TO admin;



/*Create row level security for data source*/
ALTER TABLE base.data_source ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_group_data_source on base.data_source
TO standard USING (pg_has_role(user_group, 'MEMBER'));

CREATE POLICY all_data_source on base.data_source
TO admin USING (true);



/*Create row level security for indicator group*/
ALTER TABLE base.indicator_group ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_group_indicator_group on base.indicator
TO standard USING (pg_has_role(user_group, 'MEMBER'));

CREATE POLICY all_indicator_group on base.indicator
TO admin USING (true);



/*Create row level security for indicator*/
ALTER TABLE base.indicator ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_group_indicator on base.indicator
TO standard USING (pg_has_role(user_group, 'MEMBER'));

CREATE POLICY all_indicator on base.indicator
TO admin USING (true);



/*Create row level security for parameter*/
ALTER TABLE base.parameter ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_group_parameter on base.indicator
TO standard USING (pg_has_role(user_group, 'MEMBER'));

CREATE POLICY all_parameter on base.indicator
TO admin USING (true);



/*Create row level security for batch*/
ALTER TABLE base.batch ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_group_batch on base.indicator
TO standard USING (pg_has_role(user_group, 'MEMBER'));

CREATE POLICY all_batch on base.indicator
TO admin USING (true);



/*Create row level security for session*/
ALTER TABLE base.session ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_group_session on base.indicator
TO standard USING (pg_has_role(user_group, 'MEMBER'));

CREATE POLICY all_session on base.indicator
TO admin USING (true);



/*Create row level security for session result*/
ALTER TABLE base.session_result ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_group_session_result on base.indicator
TO standard USING (pg_has_role(user_group, 'MEMBER'));

CREATE POLICY all_session_result on base.indicator
TO admin USING (true);
