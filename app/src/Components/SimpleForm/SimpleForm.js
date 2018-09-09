import React from 'react';
import { withFormik, Formik } from 'formik';
import gql from "graphql-tag";
import { graphql, compose, Mutation } from "react-apollo";
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SimpleButton from './../FormInput/SimpleButton';

class SimpleForm extends React.Component {
  render() {
      const addIndicatorMutation = gql`
    mutation addNewIndicator($indicator: IndicatorInput!) {
    createIndicator(input: { indicator: $indicator })
    {
      indicator {
        id
        name
        description
      }
    }
  }
`;
    return (
      <Mutation mutation={addIndicatorMutation}>
        {(addIndicator, { loading, error }) => (
            <React.Fragment>
          <IndicatorForm
              data={this.props.data}
              mutate={addIndicator}
          />
                {loading && <p>Loading...</p>}
                {error && <p>Error :( Please try again</p>}
            </React.Fragment>
        )}
    </Mutation>
    )
  }
}

const IndicatorFormFields = props => {
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
    <form onSubmit={handleSubmit}>
      <TextInput
        id="name"
        label="Indicator name"
        helperText=""
        placeholder="Enter indicator name"
        touched={touched.name}
        errors={errors.name}
        error={touched.name && errors.name}
        value={values.name}
        onChange={handleChange}
        onBlur={handleBlur}
      />
       <TextInput
        id="description"
        label="Indicator Description"
        helperText=""
        placeholder="Enter decription name"
        touched={touched.description}
        errors={errors.description}
        error={touched.description && errors.description}
        value={values.description}
        onChange={handleChange}
        onBlur={handleBlur}
      />
      <TextInput
          id="executionOrder"
          label="Execution Order"
          helperText=""
          numeric={true}
          touched={touched.executionOrder}
          errors={errors.executionOrder}
          error={touched.executionOrder && errors.executionOrder}
          value={values.executionOrder}
          onChange={handleChange}
          onBlur={handleBlur}
      />
      <SelectInput
        id="indicatorTypeId"
        label="Indicator Type"
        items={data.allIndicatorTypes.nodes}
        touched={touched.indicatorTypeId}
        errors={errors.indicatorTypeId}
        error={touched.indicatorTypeId && errors.indicatorTypeId}
        value={values.indicatorTypeId}
        onChange={handleChange}
        onBlur={handleBlur}
      />
      <SelectInput
        id="indicatorGroupId"
        label="Indicator Group"
        items={data.allIndicatorGroups.nodes}
        touched={touched.indicatorGroupId}
        errors={errors.indicatorGroupId}
        error={touched.indicatorGroupId && errors.indicatorGroupId}
        value={values.indicatorGroupId}
        onChange={handleChange}
        onBlur={handleBlur}
      />
      <SimpleButton
        type="reset"
        label="Reset"
        onClick={handleReset}
        disabled={!dirty || isSubmitting}
      />
      <SimpleButton
          type="submit"
          disabled={isSubmitting}
          label="Submit"
      />
    </form>
  );
};

const formikEnhancer = withFormik({
  // validationSchema: Yup.object().shape({
  //   firstName: Yup.string()
  //     .min(2, "C'mon, your name is longer than that")
  //     .required('First name is required.'),
  //   lastName: Yup.string()
  //     .min(2, "C'mon, your name is longer than that")
  //     .required('Last name is required.'),
  //   email: Yup.string()
  //     .email('Invalid email address')
  //     .required('Email is required!'),
  // }),

  mapPropsToValues: ({ indicator }) => ({
      name: '', description: '', executionOrder: 0, indicatorTypeId: "", indicatorGroupId: ""
  }),
  handleSubmit: (payload, { props, setSubmitting, setErrors }) => {
    // alert(payload.name);
    setSubmitting(false);
    props.mutate({ variables: { indicator: payload } });//, payload.description, payload.executionOrder, payload.indicatorTypeId, payload.indicatorGroupId);
  },
  displayName: 'MyForm',
});

const IndicatorForm = formikEnhancer(IndicatorFormFields);

export default SimpleForm;