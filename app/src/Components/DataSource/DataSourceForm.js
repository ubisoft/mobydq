import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SimpleButton from './../FormInput/SimpleButton';
import RouterButton from './../FormInput/RouterButton';

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
    <form onSubmit={handleSubmit} style={{ marginLeft: '60px' }}>
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
          style={{float: 'left'}}
        />
      <div>
      <div>
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
      </div>
      </div>
        <TextInput
          id="connectionString"
          label="Connection string"
          helperText=""
          placeholder=""
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
          label="Login"
          helperText=""
          placeholder=""
          touched={touched.login}
          error={touched.name && errors.login}
          value={values.login}
          onChange={handleChange}
          onBlur={handleBlur}
          style={{float: 'left'}}
        />
      <div>
      </div>
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
        <div>
          <SimpleButton type="submit" disabled={isSubmitting} label="Submit" /> &nbsp;
          <SimpleButton type="reset" label="Reset" onClick={handleReset} disabled={!dirty || isSubmitting} /> &nbsp;
          <RouterButton targetLocation='back' disabled={false} label="Cancel" />
        </div>
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
