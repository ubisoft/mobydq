import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import Select from '@material-ui/core/Select';

const SelectInput = ({
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
    <Select
      id={id}
      name={id}
      value={value}
      onChange={onChange}
    >
      <MenuItem value="">
        <em>None</em>
      </MenuItem>
      <MenuItem value={10}>Ten</MenuItem>
      <MenuItem value={20}>Twenty</MenuItem>
      <MenuItem value={30}>Thirty</MenuItem>
  </Select>
  );
};

export default SelectInput;


SelectInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
};