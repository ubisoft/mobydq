import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SaveButton from './../FormInput/SaveButton';
import ExecuteButton from './../FormInput/ExecuteButton';
import SwitchInput from './../FormInput/SwitchInput';
import SelectInput from './../FormInput/SelectInput';

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
    <div>
      <TextInput
        type="password"
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
      <SelectInput
        id="role"
        label="Role"
        items={[
          { 'id': 'standard', 'name': 'Standard' },
          { 'id': 'advanced ', 'name': 'Advanced ' },
          { 'id': 'admin', 'name': 'Admin' }
        ]}
        touched={touched.role}
        error={touched.role && errors.role}
        value={values.role}
        onChange={handleChange}
        onBlur={handleBlur}
      />
    </div>
    <div>
      <SwitchInput
        id="flagActive"
        label="Active"
        touched={touched.flagActive}
        error={touched.flagActive && errors.flagActive}
        checked={values.flagActive}
        value="flagActive"
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
    'role': Yup.string()
      .required('Role cannot be blank')
  }),
  'mapPropsToValues': (props) => props.initialFieldValues === null
    ? {
      'email': '',
      'password': '',
      'role': '',
      'flagActive': false
    }
    : /* It doesn't make sense to display the hashed password*/{
      'id': props.initialFieldValues.id,
      'email': props.initialFieldValues.email,
      'dataSourceTypeId': props.initialFieldValues.role,
      'password': '',
      'flagActive': props.initialFieldValues.flagActive
    },
  'handleSubmit': (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    delete payload.createdDate;
    delete payload.createdBy;
    delete payload.updatedDate;
    delete payload.updatedBy;
    // If the password isn't changed, it shouldn't be sent to the server
    if (payload.password === '') {
      delete payload.password;
    }
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
