import TextField from '@material-ui/TextField'
import { RadioButton, RadioButtonGroup } from '@material-ui/RadioButton'
import Checkbox from '@material-ui/Checkbox'
import SelectField from '@material-ui/SelectField'
import MenuItem from '@material-ui/MenuItem'


const renderTextField = (
  { input, label, touched, errors, ...custom },
) => (
  <TextField
    hintText={label}
    floatingLabelText={label}
    errorText={touched && error}
    {...input}
    {...custom}
  />
);

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
      <TextField
        hintText="First Name"
        floatingLabelText="First Name"
        touched={touched.firstName}
        errors={errors.firstName}
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
      <DisplayFormikState {...props} />
    </form>
  );
};