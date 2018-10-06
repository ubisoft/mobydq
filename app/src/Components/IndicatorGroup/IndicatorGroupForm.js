import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SimpleButton from './../FormInput/SimpleButton';
import RouterButton from './../FormInput/RouterButton';

const IndicatorGroupFormFields = props => {
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
          label="Indicator group name"
          helperText=""
          placeholder="Enter indicator group name"
          touched={touched.name}
          error={touched.name && errors.name}
          value={values.name}
          onChange={handleChange}
          onBlur={handleBlur}
          style={{float: 'left'}}
        />
      </div>
      <div>
        <div style={{float: 'left'}}>
          <SimpleButton type="submit" disabled={isSubmitting} label="Submit" />
          <SimpleButton type="reset" label="Reset" onClick={handleReset} disabled={!dirty || isSubmitting} />
        </div>
        <div style={{float: 'right'}}><RouterButton targetLocation='back' disabled={false} label="Cancel" /></div>
      </div>
    </form>
  );
};

const formikEnhancer = withFormik({
  validationSchema: Yup.object().shape({
    name: Yup.string()
      .required('Name cannot be blank')
  }),

  mapPropsToValues: ({ indicatorGroup }) => ({
      name: ''
  }),
  handleSubmit: (payload, { props, setSubmitting, setErrors }) => {
    setSubmitting(false);
    props.mutate({
        variables: { indicatorGroup: payload } },
        );
  },
  displayName: 'IndicatorGroupForm',
});


const EnhancedIndicatorGroupForm = formikEnhancer(IndicatorGroupFormFields);

export default EnhancedIndicatorGroupForm;