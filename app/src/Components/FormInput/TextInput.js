import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';

const TextInput = ({
  id,
  label,
  helperText,
  error,
  value,
  onChange,
  numeric,
  touched, // eslint-disable-line
  ...props
}) => <FormControl style={{ 'width': '500px' }} error={Boolean(error)}>
  <FormControlLabel
    control={
      <React.Fragment>
        <TextField
          id={id}
          label={label}
          helperText={helperText}
          onChange={onChange}
          value={value}
          type={numeric ? 'number' : 'text'}
          margin={'dense'}
          fullWidth={true}
          variant={'outlined'}
          {...props}
        />
      </React.Fragment>
    }
    label={''}
  />
  <FormHelperText>{error}</FormHelperText>
</FormControl>;
export default TextInput;

TextInput.propTypes = {
  'id': PropTypes.string.isRequired,
  'label': PropTypes.string.isRequired,
  'helperText': PropTypes.string.isRequired
};
