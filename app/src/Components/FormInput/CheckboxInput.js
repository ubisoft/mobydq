import React from 'react';
import PropTypes from 'prop-types';
import Checkbox from '@material-ui/core/Checkbox';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';

const CheckboxInput = ({
  id,
  label,
  error,
  value,
  onChange,
  ...props
}) => {
  return (
    <FormControl style={{width: '250px', margin: '15px'}} error={!!error}>
      <FormControlLabel
        control={
          <React.Fragment>
            <Checkbox
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

export default CheckboxInput;


CheckboxInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
};