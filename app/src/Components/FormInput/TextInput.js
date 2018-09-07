import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import InputFeedback from './InputFeedback';

const TextInput = ({
  id,
  label,
  helperText,
  error,
  touched,
  errors,
  value,
  onChange,
  className,
  ...props
}) => {
  return (
    <FormControlLabel
      control={
        <React.Fragment>
          <TextField
            id={id}
            label={label}
            helperText={helperText}
            onChange={onChange}
            value={value}
            // errorText={touched && errors}
            {...props}
          />
          <InputFeedback error={error} />
        </React.Fragment>
      }
      label={""}
    />
  );
};

export default TextInput;


TextInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  helperText: PropTypes.string.isRequired,
};