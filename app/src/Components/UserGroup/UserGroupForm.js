import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SaveButton from './../FormInput/SaveButton';
import ExecuteButton from './../FormInput/ExecuteButton';

const UserGroupFormFields = (props) => {
  const {
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
      <ExecuteButton onClick={() => alert('not yet implemented')}/>
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
  </form>;
};

const formikEnhancer = withFormik({
  'validationSchema': Yup.object().shape({
    'name': Yup.string()
      .required('Name cannot be blank')
  }),
  'mapPropsToValues': (props) => props.initialFieldValues === null
    ? {
      'name': ''
    }
    : {
      'id': props.initialFieldValues.userGroupId,
      'name': props.initialFieldValues.name
    },
  'handleSubmit': (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    delete payload.createdDate;
    delete payload.createdBy;
    delete payload.updatedDate;
    delete payload.updatedBy;
    let variables;
    if (props.initialFieldValues === null) {
      variables = { 'userGroup': payload };
    } else {
      variables = { 'userGroupPatch': payload, 'id': props.initialFieldValues.id };
    }
    props.mutate({
      variables
    });
  },
  'displayName': 'UserGroupForm'
});


const EnhancedUserGroupForm = formikEnhancer(UserGroupFormFields);

export default EnhancedUserGroupForm;
