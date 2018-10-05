import React from 'react';
import PropTypes from 'prop-types';
import Switch from '@material-ui/core/Switch';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';

const SwitchInput = ({
  id,
  label,
  error,
  touched,
  value,
  onChange,
  className,
  ...props
}) => {
  return (
    <FormControl style={{width: '250px', margin: '15px'}} error={!!error}>
      <FormControlLabel
        control={
          <React.Fragment>
            <Switch
              id={id}
              onChange={onChange}
              value={value}
              {...props}
            />
          </React.Fragment>
        }
        label={label}
      />
      <FormHelperText>{error}</FormHelperText>
    </FormControl>
  );
};

export default SwitchInput;


SwitchInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
};