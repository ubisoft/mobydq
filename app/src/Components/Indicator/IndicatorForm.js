import React from 'react';
import { withFormik } from 'formik';
import * as Yup from 'yup';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SimpleButton from './../FormInput/SimpleButton';
import RouterButton from './../FormInput/RouterButton';
import SwitchInput from './../FormInput/SwitchInput';

const IndicatorFormFields = props => {
  const {
    data,
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
          style={{ float: 'left' }}
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
          style={{ float: 'left' }}
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
        <div>
          <SimpleButton type="submit" disabled={isSubmitting} label="Submit"  variant='contained'/> &nbsp;
          <SimpleButton type="reset" label="Reset" onClick={handleReset} disabled={!dirty || isSubmitting}  variant='contained'/> &nbsp;
          <RouterButton targetLocation='back' disabled={false} label="Cancel" variant='contained'/>
        </div>
      </div>
    </form>
  );
};

const formikEnhancer = withFormik({
  validationSchema: Yup.object().shape({
    indicatorTypeId: Yup.number().integer()
      .min(1, 'You need to select an indicator type')
      .required('You need to select an indicator type'),
    indicatorGroupId: Yup.number().integer()
      .min(1, 'You need to select an indicator group')
      .required('You need to select an indicator group'),
    executionOrder: Yup.number().integer()
      .min(0, 'Execution order has to be a non-negative integer')
      .required('You need to input execution order.'),
    name: Yup.string()
      .required('Name cannot be blank'),
    description: Yup.string()
      .required('Description cannot be blank'),
  }),

  mapPropsToValues: (props) => (
    props.initialFieldValues === null
      ? {name: '', description: '', executionOrder: 0, indicatorTypeId: 0, indicatorGroupId: 0, flagActive: false}
      : {name: props.initialFieldValues.name, description: props.initialFieldValues.description,
        executionOrder: props.initialFieldValues.executionOrder, indicatorTypeId: props.initialFieldValues.indicatorTypeId,
        indicatorGroupId: props.initialFieldValues.indicatorGroupId, flagActive: props.initialFieldValues.flagActive}
  ),
  handleSubmit: (payload, { props, setSubmitting }) => {
    setSubmitting(false);
    props.mutate({
      variables: { indicator: payload }
    },
    );
  },
  displayName: 'IndicatorForm',
});


const EnhancedIndicatorForm = formikEnhancer(IndicatorFormFields);

export default EnhancedIndicatorForm;
