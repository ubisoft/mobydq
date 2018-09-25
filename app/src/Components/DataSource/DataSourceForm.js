import React from 'react';
import { withFormik, Formik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SimpleButton from './../FormInput/SimpleButton';
import RouterButton from './../FormInput/RouterButton';
import SwitchInput from './../FormInput/SwitchInput';

const DataSourceFormFields = props => {
  const {
    data,
    mutationCallback,
    values,
    touched,
    errors,
    dirty,
    handleChange,
    handleBlur,
    handleSubmit,
    handleReset,
    isSubmitting,
  } = props;
  return (
    <form onSubmit={handleSubmit} style={{marginLeft: '5%', marginRight: '5%', marginTop: '5%'}}>
      <div>
        <TextInput
          id="name"
          label="Data source name"
          helperText=""
          placeholder="Enter data source name"
          touched={touched.name}
          error={touched.name && errors.name}
          value={values.name}
          onChange={handleChange}
          onBlur={handleBlur}
          style={{float: 'left'}}
        />
        <TextInput
          id="connectionString"
          label="Data source connection string"
          helperText=""
          placeholder="Enter data connection string"
          touched={touched.connectionString}
          error={touched.name && errors.connectionString}
          value={values.connectionString}
          onChange={handleChange}
          onBlur={handleBlur}
        />
        </div>
        <div>
        <TextInput
          id="login"
          label="Data source login"
          helperText=""
          placeholder="Enter data source login"
          touched={touched.login}
          error={touched.name && errors.login}
          value={values.login}
          onChange={handleChange}
          onBlur={handleBlur}
          style={{float: 'left'}}
        />
        <TextInput
          id="password"
          label="Data source password"
          helperText=""
          placeholder="Enter data source password"
          touched={touched.password}
          error={touched.password && errors.password}
          value={values.password}
          onChange={handleChange}
          onBlur={handleBlur}
        />
      </div>
      <div>
        <div style={{float: 'left'}}>
          <SimpleButton type="submit" disabled={isSubmitting} label="Submit" />
          <SimpleButton tyloginpe="reset" label="Reset" onClick={handleReset} disabled={!dirty || isSubmitting} />
        </div>
        <div style={{float: 'right'}}><RouterButton targetLocation='back' disabled={false} label="Cancel" /></div>
      </div>
    </form>
  );
};

const formikEnhancer = withFormik({
  validationSchema: Yup.object().shape({
    name: Yup.string()
      .required('Name cannot be blank'),
    connectionString: Yup.string()
      .required('Connection string cannot be blank'),
    login: Yup.string()
      .required('Login cannot be blank')
  }),

  mapPropsToValues: ({ dataSource }) => ({
      name: '', connectionString: '', login: '', password: ''
  }),
  handleSubmit: (payload, { props, setSubmitting, setErrors }) => {
    setSubmitting(false);
    props.mutate({
        variables: { dataSource: payload } },
        );
  },
  displayName: 'DataSourceForm',
});


const EnhancedDataSourceForm = formikEnhancer(DataSourceFormFields);

export default EnhancedDataSourceForm;