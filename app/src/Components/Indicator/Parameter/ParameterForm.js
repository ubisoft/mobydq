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
        id="id"
        label="id"
        helperText=""
        placeholder=""
        disabled={true}
        touched={touched.id}
        error={touched.id && errors.id}
        value={values.id}
        onChange={handleChange}
        onBlur={handleBlur}
      />
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
      'id': '',
      'value': '',
      'description': '',
      'parameterTypeId': 0
    }
    : {
      'id': props.initialFieldValues.id,
      'value': props.initialFieldValues.value,
      'parameterTypeId': props.initialFieldValues.parameterTypeId,
      'createdDate': props.initialFieldValues.createdDate,
      'createdBy': props.initialFieldValues.userByCreatedById.email,
      'updatedDate': props.initialFieldValues.updatedDate,
      'updatedBy': props.initialFieldValues.userByUpdatedById.email
    },
  'handleSubmit': (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    delete payload.createdDate;
    delete payload.createdBy;
    delete payload.updatedDate;
    delete payload.updatedBy;
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
