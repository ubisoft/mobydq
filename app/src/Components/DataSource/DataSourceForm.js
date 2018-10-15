import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SimpleButton from './../FormInput/SimpleButton';

const DataSourceFormFields = props => {
  const {
    data,
    values,
    touched,
    errors,
    handleChange,
    handleBlur,
    handleSubmit,
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
          <SimpleButton type="submit" disabled={isSubmitting} label='Submit' variant='contained'/> &nbsp;
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

  mapPropsToValues: (props) => (
    props.initialFieldValues === null
      ? {name: '', connectionString: '', dataSourceTypeId: '', login: '', password: ''}
      : {name: props.initialFieldValues.name, connectionString: props.initialFieldValues.connectionString,
          dataSourceTypeId: props.initialFieldValues.dataSourceTypeId,
          login: props.initialFieldValues.login, password: props.initialFieldValues.password}
  ),
  handleSubmit: (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    let variables;
    if (props.initialFieldValues === null) {
        variables = { dataSource: payload};
    } else {
        variables = { dataSourcePatch: payload, id: props.initialFieldValues.id };
    }
    props.mutate({
      variables: variables
    });
  },
  displayName: 'DataSourceForm',
});


const EnhancedDataSourceForm = formikEnhancer(DataSourceFormFields);

export default EnhancedDataSourceForm;
