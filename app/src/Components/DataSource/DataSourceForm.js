import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';

const DataSourceFormFields = (props) => {
  const {
    data,
    values,
    touched,
    errors,
    handleChange,
    handleBlur,
    handleSubmit,
    isSubmitting
  } = props;
  return (
    <form onSubmit={handleSubmit} style={{ 'marginLeft': '60px' }}>
      <div>
        <TextInput
          id="name"
          label="Name"
          helperText=""
          placeholder=""
          touched={touched.name}
          error={touched.name && errors.name}
          value={values.name}
          onChange={handleChange}
          onBlur={handleBlur}
        />
        <br />
        <SelectInput
          id="dataSourceTypeId"
          label="Type"
          items={data.allDataSourceTypes.nodes}
          touched={touched.dataSourceTypeId}
          error={touched.dataSourceTypeId && errors.dataSourceTypeId}
          value={values.dataSourceTypeId}
          onChange={handleChange}
          onBlur={handleBlur}
        />
        <br />
        <textarea
          id="connectionString"
          label="Connection string"
          helperText=""
          placeholder="Connection string"
          touched={touched.connectionString}
          error={touched.name && errors.connectionString}
          value={values.connectionString}
          onChange={handleChange}
          onBlur={handleBlur}
        />
        <br />
        <TextInput
          id="login"
          label="Login"
          helperText=""
          placeholder=""
          touched={touched.login}
          error={touched.name && errors.login}
          value={values.login}
          onChange={handleChange}
          onBlur={handleBlur}
        />
        <br />
        <TextInput
          id="password"
          label="Password"
          helperText=""
          placeholder=""
          touched={touched.password}
          error={touched.password && errors.password}
          value={values.password}
          onChange={handleChange}
          onBlur={handleBlur}
        />
      </div>
      <div>
        <Button type="submit" disabled={isSubmitting} variant="contained" color={'secondary'}>
          <SaveIcon />
          Save
        </Button>
      </div>
    </form>
  );
};

const formikEnhancer = withFormik({
  'validationSchema': Yup.object().shape({
    'name': Yup.string()
      .required('Name cannot be blank'),
    'connectionString': Yup.string()
      .required('Connection string cannot be blank'),
    'login': Yup.string()
      .required('Login cannot be blank')
  }),

  'mapPropsToValues': (props) => props.initialFieldValues === null
    ? { 'name': '', 'connectionString': '', 'dataSourceTypeId': '', 'login': '', 'password': '' }
    : { 'name': props.initialFieldValues.name,
      'connectionString': props.initialFieldValues.connectionString,
      'dataSourceTypeId': props.initialFieldValues.dataSourceTypeId,
      'login': props.initialFieldValues.login,
      'password': props.initialFieldValues.password },
  'handleSubmit': (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    let variables;
    if (props.initialFieldValues === null) {
      variables = { 'dataSource': payload };
    } else {
      variables = { 'dataSourcePatch': payload, 'id': props.initialFieldValues.id };
    }
    props.mutate({
      variables
    });
  },
  'displayName': 'DataSourceForm'
});


const EnhancedDataSourceForm = formikEnhancer(DataSourceFormFields);

export default EnhancedDataSourceForm;
