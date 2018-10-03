import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';

const DateInput = ({
  id,
  label,
  helperText,
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
             errorText={touched && errors}
             {...props}
           />
           <InputFeedback error={error} />
        </React.Fragment>
      }
      label={""}
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