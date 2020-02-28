/*Connect to database*/
\connect mobydq



/*
Create anonymous user role
The anonymous role is the default role used to query the database for non authenticated users.
It grants permissions to read data in to the Public user group.
*/
CREATE ROLE anonymous;
GRANT user_group_1 TO anonymous;  /*Grant Public user group to anonymous*/

/*base schema*/
GRANT USAGE ON SCHEMA base TO anonymous;
GRANT SELECT ON base.user TO anonymous;
GRANT SELECT ON base.user_group TO anonymous;
GRANT SELECT ON base.user_group_membership TO anonymous;
GRANT SELECT ON base.data_source_type TO anonymous;
GRANT SELECT ON base.data_source TO anonymous;
GRANT SELECT ON base.indicator_type TO anonymous;
GRANT SELECT ON base.indicator_group TO anonymous;
GRANT SELECT ON base.indicator TO anonymous;
GRANT SELECT ON base.parameter_type TO anonymous;
GRANT SELECT ON base.parameter TO anonymous;
GRANT SELECT ON base.batch TO anonymous;
GRANT SELECT ON base.session TO anonymous;
GRANT SELECT ON base.log TO anonymous;
GRANT SELECT ON base.notification TO anonymous;

/*Dashboard views*/
GRANT SELECT ON base.nb_indicators TO anonymous;
GRANT SELECT ON base.batch_status TO anonymous;
GRANT SELECT ON base.batch_statistics TO anonymous;
GRANT SELECT ON base.session_status TO anonymous;
GRANT SELECT ON base.session_statistics TO anonymous;



/*
Create standard user role
The standard role is the default role for all users who wish to create and manage data quality indicators.
*/
CREATE ROLE standard;
GRANT anonymous TO standard;

/*base schema*/
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA base TO standard;
GRANT SELECT ON base.password TO standard;
GRANT SELECT ON base.data_source_password TO standard;
GRANT SELECT ON base.configuration TO standard;
GRANT INSERT, UPDATE, DELETE, REFERENCES ON base.indicator_group TO standard;
GRANT INSERT, UPDATE, DELETE, REFERENCES ON base.indicator TO standard;
GRANT INSERT, UPDATE, DELETE, REFERENCES ON base.parameter TO standard;
GRANT INSERT, UPDATE, DELETE, REFERENCES ON base.batch TO standard;
GRANT INSERT, UPDATE, DELETE, REFERENCES ON base.session TO standard;
GRANT INSERT, UPDATE, DELETE, REFERENCES ON base.log TO standard;
GRANT INSERT, UPDATE, DELETE, REFERENCES ON base.notification TO standard;
GRANT EXECUTE ON FUNCTION base.test_data_source TO standard;
GRANT EXECUTE ON FUNCTION base.execute_batch TO standard;
GRANT EXECUTE ON FUNCTION base.mark_all_notifications_as_read TO standard;



/*
Create advanced user role
The advanced role is the role used for users who wish to create and manage data sources.
In addition to the permissions of the standard role, it grants permissions to create, update and delete data sources.
*/
CREATE ROLE advanced;
GRANT standard TO advanced;

/*base schema*/
GRANT INSERT, UPDATE, DELETE, REFERENCES ON base.configuration TO advanced;
GRANT INSERT, UPDATE, DELETE, REFERENCES ON base.data_source TO advanced;
GRANT EXECUTE ON FUNCTION base.kill_test_data_source TO advanced;
GRANT EXECUTE ON FUNCTION base.kill_execute_batch TO advanced;



/*
Create admin user role
The admin role is used to manage application users and configuration.
It grants the same permissions as the advanced role, plus the permissions to read, write and delete the following objects:
Users, User Groups, Data Source Types, Indicator Types, Parameter Types
*/
CREATE ROLE admin;
GRANT advanced TO admin;

/*base schema*/
GRANT INSERT, UPDATE, DELETE ON base.user TO admin;
GRANT INSERT, UPDATE, DELETE ON base.password TO admin;
GRANT INSERT, UPDATE, DELETE ON base.user_group TO admin;
GRANT INSERT, UPDATE, DELETE ON base.user_group_membership TO admin;
GRANT INSERT, UPDATE, DELETE ON base.data_source_type TO admin;
GRANT INSERT, UPDATE, DELETE ON base.indicator_type TO admin;
GRANT INSERT, UPDATE, DELETE ON base.parameter_type TO admin;

/*Grant admin role to default user*/
GRANT admin TO user_1;



/*Create row level security policies*/
ALTER TABLE base.data_source ENABLE ROW LEVEL SECURITY;
ALTER TABLE base.indicator_group ENABLE ROW LEVEL SECURITY;
ALTER TABLE base.indicator ENABLE ROW LEVEL SECURITY;
ALTER TABLE base.parameter ENABLE ROW LEVEL SECURITY;
ALTER TABLE base.batch ENABLE ROW LEVEL SECURITY;
ALTER TABLE base.session ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_group_policy on base.data_source FOR ALL TO PUBLIC
USING (pg_has_role('user_group_' || user_group_id, 'MEMBER'));

CREATE POLICY user_group_policy on base.indicator_group FOR ALL TO PUBLIC
USING (pg_has_role('user_group_' || user_group_id, 'MEMBER'));

CREATE POLICY user_group_policy on base.indicator FOR ALL TO PUBLIC
USING (pg_has_role('user_group_' || user_group_id, 'MEMBER'));

CREATE POLICY user_group_policy on base.parameter FOR ALL TO PUBLIC
USING (pg_has_role('user_group_' || user_group_id, 'MEMBER'));

CREATE POLICY user_group_policy on base.batch FOR ALL TO PUBLIC
USING (pg_has_role('user_group_' || user_group_id, 'MEMBER'));

CREATE POLICY user_group_policy on base.session FOR ALL TO PUBLIC
USING (pg_has_role('user_group_' || user_group_id, 'MEMBER'));

CREATE POLICY user_policy on base.notification FOR ALL TO PUBLIC
USING (created_by_id=base.get_current_user_id());