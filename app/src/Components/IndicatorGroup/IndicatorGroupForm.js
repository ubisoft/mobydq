import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SimpleButton from './../FormInput/SimpleButton';
import RouterButton from './../FormInput/RouterButton';

const IndicatorGroupFormFields = props => {
  const {
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
      .required('Name cannot be blank')
  }),

  mapPropsToValues: () => ({
    name: ''
  }),
  handleSubmit: (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    props.mutate({
      variables: { indicatorGroup: payload }
    });
  },
  displayName: 'IndicatorGroupForm',
});


const EnhancedIndicatorGroupForm = formikEnhancer(IndicatorGroupFormFields);

export default EnhancedIndicatorGroupForm;
