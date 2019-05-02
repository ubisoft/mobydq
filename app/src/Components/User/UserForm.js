import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SaveButton from './../FormInput/SaveButton';
import ExecuteButton from './../FormInput/ExecuteButton';

const UserFormFields = (props) => {
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
    <div style={{
      'marginTop': '10px',
      'marginBottom': '30px'
    }}>
      <SaveButton disabled={isSubmitting}/>
      <ExecuteButton onClick={() => alert('not yet implemented')}/>
    </div>
    <div>
      <TextInput
        id="email"
        label="Email"
        helperText=""
        placeholder=""
        touched={touched.email}
        error={touched.email && errors.email}
        value={values.email}
        onChange={handleChange}
        onBlur={handleBlur}
      />
    </div>
  </form>;
};

const formikEnhancer = withFormik({
  'validationSchema': Yup.object().shape({
    'email': Yup.string()
      .required('Email cannot be blank'),
    'active': Yup.bool()
      .required('Active cannot be blank')
  }),
  'mapPropsToValues': (props) => props.initialFieldValues === null
    ? {
      'email': '',
      'active': true
    }
    : {
      'id': props.initialFieldValues.id,
      'email': props.initialFieldValues.email,
      'active': props.initialFieldValues.flagActive
    },
  'handleSubmit': (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    delete payload.createdDate;
    delete payload.createdBy;
    delete payload.updatedDate;
    delete payload.updatedBy;
    let variables;
    if (props.initialFieldValues === null) {
      variables = { 'user': payload };
    } else {
      variables = {
        'userPatch': payload,
        'id': props.initialFieldValues.id
      };
    }
    props.mutate({
      variables
    });
  },
  'displayName': 'UserForm'
});


const EnhancedUserForm = formikEnhancer(UserFormFields);

export default EnhancedUserForm;
