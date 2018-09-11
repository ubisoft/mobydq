import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import InputFeedback from './InputFeedback';

const DateInput = ({
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
    <FormControlLabel style={{width: '250px', margin: '15px'}}
      control={
        <React.Fragment>
          <TextField
            id={id}
            label={label}
            type="date"
            value={value}
            InputLabelProps={{
              shrink: true,
            }}
            helperText={helperText}
            onChange={onChange}
            errorText={touched && errors}
            {...props}
          />
          <InputFeedback error={error} />
        </React.Fragment>
      }
      label={""}
    />
  );
};

export default DateInput;


DateInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  helperText: PropTypes.string.isRequired,
};