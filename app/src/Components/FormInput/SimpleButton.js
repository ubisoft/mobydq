import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';

const SimpleButton = ({
  type,
  disabled,
  label,
  onClick
}) => {
  let color = 'default';
    switch(type) {
      case 'submit':
        color = 'primary';
        break;
      case 'create':
        color = 'primary';
        break;
      case 'reset':
        color = 'secondary';
        break;
      case 'cancel':
        color = 'default';
        break;
    }
  return (
    <Button type={type} disabled={disabled} variant="contained" color={color} onClick={onClick}>
      {label}
    </Button>
  )
}

export default SimpleButton;

SimpleButton.propTypes = {
  type: PropTypes.string.isRequired,
  disabled: PropTypes.bool.isRequired,
  label: PropTypes.string.isRequired,
};