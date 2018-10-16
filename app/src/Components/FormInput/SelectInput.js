import React from 'react';
import PropTypes from 'prop-types';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const SelectInput = ({
  id,
  label,
  items,
  error,
  value,
  onChange,
  ...props
}) => {
  return (
    <FormControl style={{width: '240px', margin: '15px', marginLeft: '0px'}} error={!!error}>
      <InputLabel htmlFor={id}>{label}</InputLabel>
      <Select
        id={id}
        name={id}
        value={value}
        onChange={onChange}
        inputProps={{
          id: { id }
        }}
        {...props}
      >
        <MenuItem value="">
          <em>Select..</em>
        </MenuItem>
        {items.map((item) => {
          return (<MenuItem key={item.id} value={item.id}>{item.name}</MenuItem>)
        })
        }
      </Select>
      <FormHelperText>{error}</FormHelperText>
    </FormControl>
  );
};

export default SelectInput;


SelectInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  items: PropTypes.array.isRequired,
};