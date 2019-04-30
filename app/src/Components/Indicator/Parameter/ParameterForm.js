import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../../FormInput/TextInput';
import SelectInput from './../../FormInput/SelectInput';
import SwitchInput from './../../FormInput/SwitchInput';
import SaveButton from './../../FormInput/SaveButton';
import DeleteButton from './../../FormInput/DeleteButton';

const ParameterFormFields = (props) => {
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
      <DeleteButton onClick={() => alert('not yet implemented')} />
    </div>
    <div>
      <TextInput
        id="value"
        label="value"
        helperText=""
        placeholder=""
        touched={touched.value}
        error={touched.value && errors.value}
        value={values.value}
        onChange={handleChange}
        onBlur={handleBlur}
        multiline={false}
      />
    </div>
    <div>
      <SelectInput
        id="parameterTypeId"
        label="Type"
        items={data.allParameterTypes.nodes}
        touched={touched.parameterTypeId}
        error={touched.parameterTypeId && errors.parameterTypeId}
        value={values.parameterTypeId}
        onChange={handleChange}
        onBlur={handleBlur}
      />
    </div>
    <div>
      <TextInput
        id="indicatorId"
        label="indicatorId"
        helperText=""
        placeholder=""
        disabled={true}
        touched={touched.indicatorId}
        error={touched.id && errors.indicatorId}
        value={values.indicatorId}
        onChange={handleChange}
        onBlur={handleBlur}
      />
    </div>
  </form>;
};

const formikEnhancer = withFormik({
  'validationSchema': Yup.object().shape({
    'parameterTypeId': Yup.number().integer()
      .min(1, 'You need to select an parameter type')
      .required('You need to select an parameter type'),
    'value': Yup.string()
      .required('Value cannot be blank')
  }),

  'mapPropsToValues': (props) => props.initialFieldValues === null
    ? {
      'indicatorId': props.indicatorId,
      'value': '',
      'parameterTypeId': 0
    }
    : {
      'indicatorId': props.initialFieldValues.indicatorId,
      'value': props.initialFieldValues.value,
      'parameterTypeId': props.initialFieldValues.parameterTypeId
    },
  'handleSubmit': (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    let variables;
    if (props.initialFieldValues === null) {
      variables = { 'parameter': payload };
    } else {
      variables = { 'parameterPatch': payload, 'id': props.initialFieldValues.id };
    }
    props.mutate({
      variables
    });
  },
  'displayName': 'ParameterForm'
});


const EnhancedParameterForm = formikEnhancer(ParameterFormFields);

export default EnhancedParameterForm;
