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
}) => <FormControl style={{ 'width': '500px' }} error={Boolean(error)}>
  <FormControlLabel
    control={
      <React.Fragment>
        <TextField
          id={id}
          label={label}
          error={Boolean(error)}
          type="date"
          value={value}
          InputLabelProps={{
            'shrink': true
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
</FormControl>;
export default DateInput;


DateInput.propTypes = {
  'id': PropTypes.string.isRequired,
  'label': PropTypes.string.isRequired,
  'helperText': PropTypes.string.isRequired
};
