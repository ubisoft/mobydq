import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SwitchInput from './../FormInput/SwitchInput';
import SaveButton from './../FormInput/SaveButton';
import ExecuteButton from './../FormInput/ExecuteButton';

const IndicatorFormFields = (props) => {
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
      <ExecuteButton disabled={isSubmitting} />
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
      <TextInput
        id="description"
        label="Description"
        helperText=""
        placeholder=""
        touched={touched.description}
        error={touched.description && errors.description}
        value={values.description}
        onChange={handleChange}
        onBlur={handleBlur}
        multiline={true}
        rows={5}
      />
    </div>
    <div>
      <SelectInput
        id="indicatorTypeId"
        label="Type"
        items={data.allIndicatorTypes.nodes}
        touched={touched.indicatorTypeId}
        error={touched.indicatorTypeId && errors.indicatorTypeId}
        value={values.indicatorTypeId}
        onChange={handleChange}
        onBlur={handleBlur}
      />
    </div>
    <div>
      <SelectInput
        id="indicatorGroupId"
        label="Group"
        items={data.allIndicatorGroups.nodes}
        touched={touched.indicatorGroupId}
        error={touched.indicatorGroupId && errors.indicatorGroupId}
        value={values.indicatorGroupId}
        onChange={handleChange}
        onBlur={handleBlur}
      />
    </div>
    <div>
      <TextInput
        id="executionOrder"
        label="Execution Order"
        helperText=""
        numeric={true}
        touched={touched.executionOrder}
        error={touched.executionOrder && errors.executionOrder}
        value={values.executionOrder}
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
    'indicatorTypeId': Yup.number().integer()
      .min(1, 'You need to select an indicator type')
      .required('You need to select an indicator type'),
    'indicatorGroupId': Yup.number().integer()
      .min(1, 'You need to select an indicator group')
      .required('You need to select an indicator group'),
    'executionOrder': Yup.number().integer()
      .min(0, 'Execution order has to be a non-negative integer')
      .required('You need to input execution order.'),
    'name': Yup.string()
      .required('Name cannot be blank'),
    'description': Yup.string()
      .required('Description cannot be blank')
  }),

  'mapPropsToValues': (props) => props.initialFieldValues === null
    ? {
        'name': '',
        'description': '',
        'executionOrder': 0,
        'indicatorTypeId': 0,
        'indicatorGroupId': 0,
        'flagActive': false
      }
    : {
        'name': props.initialFieldValues.name,
        'description': props.initialFieldValues.description,
        'executionOrder': props.initialFieldValues.executionOrder,
        'indicatorTypeId': props.initialFieldValues.indicatorTypeId,
        'indicatorGroupId': props.initialFieldValues.indicatorGroupId,
        'flagActive': props.initialFieldValues.flagActive,
        'createdDate': props.initialFieldValues.createdDate,
        'createdBy': props.initialFieldValues.userByCreatedById.email,
        'updatedDate': props.initialFieldValues.updatedDate,
        'updatedBy': props.initialFieldValues.userByUpdatedById.email
      },
  'handleSubmit': (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    let variables;
    if (props.initialFieldValues === null) {
      variables = { 'indicator': payload };
    } else {
      variables = { 'indicatorPatch': payload, 'id': props.initialFieldValues.id };
    }
    props.mutate({
      variables
    });
  },
  'displayName': 'IndicatorForm'
});


const EnhancedIndicatorForm = formikEnhancer(IndicatorFormFields);

export default EnhancedIndicatorForm;
