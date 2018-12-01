import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';

const IndicatorGroupFormFields = (props) => {
  const {
    values,
    touched,
    errors,
    handleChange,
    handleBlur,
    handleSubmit,
    isSubmitting
  } = props;
  return <form onSubmit={handleSubmit} style={{ 'marginLeft': '60px' }}>
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
      <Button type="submit" disabled={isSubmitting} variant="contained" color={'secondary'}>
        <SaveIcon />
        Save
      </Button>
    </div>
  </form>;
};

const formikEnhancer = withFormik({
  'validationSchema': Yup.object().shape({
    'name': Yup.string()
      .required('Name cannot be blank')
  }),
  'mapPropsToValues': (props) => props.initialFieldValues === null
    ? { 'name': '' }
    : { 'name': props.initialFieldValues.name },
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
