import React from 'react';
import PropTypes from 'prop-types';
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import InputFeedback from './InputFeedback';

const CheckboxInput = ({
  id,
  label,
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
          <Checkbox
            id={id}
            onChange={onChange}
            errorText={touched && errors}
            value={value}
            {...props}
          />
          < InputFeedback error={error} />
        </React.Fragment>
      }
      label={label}
    />
  );
};

export default CheckboxInput;


CheckboxInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
};