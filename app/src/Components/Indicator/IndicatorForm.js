import React from 'react';
import { Query } from "react-apollo";
import gql from "graphql-tag";
import { graphql, compose, Mutation } from "react-apollo";
import { withFormik, Formik } from 'formik';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import DataTable from '../Dashboard/DataTable';
import SimpleForm from '../SimpleForm/SimpleForm';

import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SimpleButton from './../FormInput/SimpleButton';
import IndicatorRepository  from './../../repository/IndicatorRepository';

const IndicatorForm = () => (
  <Query
    query={IndicatorRepository.getFormDropdownData()}
  >
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;
      return(
       <Mutation mutation={IndicatorRepository.insertIndicator()}>
        {(addIndicator, { loading, error }) => (
          <React.Fragment>
            <EnhancedIndicatorForm
              data={data}
              mutate={addIndicator}
            />
            {loading && <p>Loading...</p>}
            {error && <p>Error :( Please try again</p>}
          </React.Fragment>
        )}
        </Mutation>
      );
    }}
  </Query>
);

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
    <form onSubmit={handleSubmit} style={{marginLeft: '5%', marginRight: '5%', marginTop: '5%'}}>
      <div>
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
          style={{float: 'left'}}
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
      </div>
      <div>
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
          style={{float: 'left'}}
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
      </div>
      <div>
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
      </div>
      <div>
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
      </div>
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


const EnhancedIndicatorForm = formikEnhancer(IndicatorFormFields);

export default IndicatorForm;
