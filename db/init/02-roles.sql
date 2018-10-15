/*Create user roles and grant the permission*/
\connect mobydq

/*Create superuser and grant permission for everything*/
CREATE ROLE super_admin;
GRANT ALL ON ALL TABLES IN SCHEMA base TO super_admin;

/*policy for indicator_group*/
CREATE POLICY super_admin_indicator_all ON
  base.indicator_group
FOR ALL
TO super_admin
USING (
  true
);

/*policy for indicator*/
CREATE POLICY super_admin_indicator_group_all ON
  base.indicator
FOR ALL
TO super_admin
USING (
  true
);

/*policy for parameter*/
CREATE POLICY super_admin_parameter_all ON
  base.parameter
FOR ALL
TO super_admin
USING (
  true
);

/*policies for data_source*/
CREATE POLICY super_admin_data_source_all ON
  base.data_source
FOR ALL
TO super_admin
USING (
  true
);

/*policy for session*/
CREATE POLICY super_admin_session_all ON
  base.session
FOR ALL
TO super_admin
USING (
  true
);

/*policy for session_result*/
CREATE POLICY super_admin_session_result_all ON
  base.session_result
FOR ALL
TO super_admin
USING (
  true
);

/*policy for batch*/
CREATE POLICY super_admin_batch_all ON
  base.batch
FOR ALL
TO super_admin
USING (
  true
);
