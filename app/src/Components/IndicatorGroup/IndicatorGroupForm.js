import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SaveButton from './../FormInput/SaveButton';
import ExecuteButton from './../FormInput/ExecuteButton';

const IndicatorGroupFormFields = (props) => {
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
    <div>
      <SelectInput
        id="userGroupId"
        label="User Group"
        items={data.allUserGroups.nodes}
        touched={touched.userGroupId}
        error={touched.userGroupId && errors.userGroupId}
        value={values.userGroupId}
        onChange={handleChange}
        onBlur={handleBlur}
      />
    </div>
  </form>;
};

const formikEnhancer = withFormik({
  'validationSchema': Yup.object().shape({
    'name': Yup.string()
      .required('Name cannot be blank'),
    'userGroupId': Yup.string()
      .required('User Group cannot be blank')
  }),
  'mapPropsToValues': (props) => props.initialFieldValues === null
    ? {
      'name': '',
      'userGroupId': ''
    }
    : {
      'name': props.initialFieldValues.name,
      'userGroupId': props.initialFieldValues.userGroupId
    },
  'handleSubmit': (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    let variables;
    if (props.initialFieldValues === null) {
      variables = { 'indicatorGroup': payload };
    } else {
      variables = { 'indicatorGroupPatch': payload, 'id': props.initialFieldValues.id };
    }
    props.mutate({
      variables
    });
  },
  'displayName': 'IndicatorGroupForm'
});


const EnhancedIndicatorGroupForm = formikEnhancer(IndicatorGroupFormFields);

export default EnhancedIndicatorGroupForm;
