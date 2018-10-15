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
          <SimpleButton type="submit" disabled={isSubmitting} label="Submit" variant='contained'/> &nbsp;
          <SimpleButton type="reset" label="Reset" onClick={handleReset} disabled={!dirty || isSubmitting} variant='contained'/> &nbsp;
          <RouterButton targetLocation='back' disabled={false} label="Cancel" variant='contained'/>
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
  mapPropsToValues: (props) => (
      props.initialFieldValues === null
    ? {name: ''}
    : {name: props.initialFieldValues.name}
  ),
  handleSubmit: (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    let variables;
    if (props.initialFieldValues === null) {
        variables = { indicatorGroup: payload};
    } else {
        variables = { indicatorGroupPatch: payload, id: props.initialFieldValues.id };
    }
    props.mutate({
      variables: variables
    });
  },
  displayName: 'IndicatorGroupForm',
});


const EnhancedIndicatorGroupForm = formikEnhancer(IndicatorGroupFormFields);

export default EnhancedIndicatorGroupForm;
