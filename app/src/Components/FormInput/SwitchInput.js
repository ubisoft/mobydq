import React from 'react';
import PropTypes from 'prop-types';
import Switch from '@material-ui/core/Switch';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import InputFeedback from './InputFeedback';

const SwitchInput = ({
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
          <Switch
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

export default SwitchInput;


SwitchInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
};