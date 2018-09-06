import React from 'react';
import { render } from 'react-dom';
import { withFormik } from 'formik'

import TextField from '@material-ui/core/TextField'
import Checkbox from '@material-ui/core/Checkbox'


class SimpleForm extends React.Component {

  render() {
     return(
        <MyEnhancedForm
          indicator={{ name: '', description: '' }}
        />
     )
  }
}

const InputFeedback = ({ error }) =>
  error ? (
    <div className="input-feedback">{error}</div>
  ) : null;

const Label = ({
  error,
  className,
  children,
  ...props
}) => {
  return (
    <label className="label" {...props}>
      {children}
    </label>
  );
};

const TextInput = ({
  id,
  label,
  helperText,
  error,
  value,
  onChange,
  className,
  ...props
}) => {
  return (
    <div>
      <TextField
        id={id}
        label={label}
        helperText={helperText}
        onChange={onChange}
        // errorText={touched && errors}
        {...props}
      />
      <InputFeedback error={error} />
    </div>
  );
};

const MyForm = props => {
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
    <form onSubmit={handleSubmit}>
      <TextInput
        id="name"
        label="Indicator name"
        helperText=""
        placeholder="Enter indicator name"
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
        error={touched.description && errors.description}
        value={values.description}
        onChange={handleChange}
        onBlur={handleBlur}
      />
      <button
        type="button"
        className="outline"
        onClick={handleReset}
        disabled={!dirty || isSubmitting}
      >
        Reset
      </button>
      <button type="submit" disabled={isSubmitting}>
        Submit
      </button>
      {/*<DisplayFormikState {...props} />*/}
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
    ...indicator,
  }),
  handleSubmit: (payload, { setSubmitting }) => {
    alert(payload.name);
    setSubmitting(false);
  },
  displayName: 'MyForm',
});


const MyEnhancedForm = formikEnhancer(MyForm);

export default SimpleForm;