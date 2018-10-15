import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';

const DateInput = ({
  id,
  label,
  helperText,
  error,
  value,
  touched, // eslint-disable-line
  onChange,
  ...props
}) => {
  return (
   <FormControl style={{width: '250px', margin: '15px'}} error={!!error}>
     <FormControlLabel
       control={
         <React.Fragment>
           <TextField
              id={id}
              label={label}
              error={!!error}
              type="date"
              value={value}
              InputLabelProps={{
                shrink: true,
              }}
              helperText={helperText}
              onChange={onChange}
              {...props}
           />
           <FormHelperText>{error}</FormHelperText>
        </React.Fragment>
      }
      label={''}
    />
   <FormHelperText>{error}</FormHelperText>
   </FormControl>
  );
};

export default DateInput;


DateInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  helperText: PropTypes.string.isRequired,
};