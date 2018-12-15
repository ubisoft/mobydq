import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SaveButton from './../FormInput/SaveButton';
import ExecuteButton from './../FormInput/ExecuteButton';
import DeleteButton from './../FormInput/DeleteButton';

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
  return <form onSubmit={handleSubmit} style={{ 'marginLeft': '50px' }}>
    <div style={{ 'marginTop': '10px', 'marginBottom': '30px' }}>
      <SaveButton disabled={isSubmitting} />
      <ExecuteButton disabled={isSubmitting} />
      <DeleteButton disabled={isSubmitting} />
    </div>
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
    </div>
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
    <div>
      <TextInput
        id="connectionString"
        label="Connection string"
        helperText=""
        placeholder="Connection string"
        touched={touched.connectionString}
        error={touched.connectionString && errors.connectionString}
        value={values.connectionString}
        onChange={handleChange}
        onBlur={handleBlur}
        multiline={true}
        rows={5}
      />
    </div>
    <div>
      <TextInput
        id="login"
        label="Login"
        helperText=""
        placeholder=""
        touched={touched.login}
        error={touched.login && errors.login}
        value={values.login}
        onChange={handleChange}
        onBlur={handleBlur}
      />
    </div>
    <div>
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
      <TextInput
        id="connectivityStatus"
        label="Connectivity status"
        helperText=""
        placeholder=""
        touched={touched.connectivityStatus}
        error={touched.connectivityStatus && errors.connectivityStatus}
        value={values.connectivityStatus}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={true}
        variant={'filled'}
      />
    </div>
    <div>
      <TextInput
        id="createdDate"
        label="Created Date"
        helperText=""
        placeholder=""
        touched={touched.createdDate}
        error={touched.createdDate && errors.createdDate}
        value={values.createdDate}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={true}
        variant={'filled'}
      />
    </div>
    <div>
      <TextInput
        id="createdBy"
        label="Created By"
        helperText=""
        placeholder=""
        touched={touched.createdBy}
        error={touched.createdBy && errors.createdBy}
        value={values.createdBy}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={true}
        variant={'filled'}
      />
    </div>
    <div>
      <TextInput
        id="updatedDate"
        label="Updated Date"
        helperText=""
        placeholder=""
        touched={touched.updatedDate}
        error={touched.updatedDate && errors.updatedDate}
        value={values.updatedDate}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={true}
        variant={'filled'}
      />
    </div>
    <div>
      <TextInput
        id="updatedBy"
        label="Updated By"
        helperText=""
        placeholder=""
        touched={touched.updatedBy}
        error={touched.updatedBy && errors.updatedBy}
        value={values.updatedBy}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={true}
        variant={'filled'}
      />
    </div>
  </form>
  ;
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
    ? {
        'name': '',
        'connectionString': '',
        'dataSourceTypeId': '',
        'login': '',
        'password': ''
      }
    : {
        'name': props.initialFieldValues.name,
        'connectionString': props.initialFieldValues.connectionString,
        'dataSourceTypeId': props.initialFieldValues.dataSourceTypeId,
        'login': props.initialFieldValues.login,
        'password': props.initialFieldValues.password,
        'createdDate': props.initialFieldValues.createdDate,
        'createdBy': props.initialFieldValues.userByCreatedById.email,
        'updatedDate': props.initialFieldValues.updatedDate,
        'updatedBy': props.initialFieldValues.userByUpdatedById.email
      },
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
