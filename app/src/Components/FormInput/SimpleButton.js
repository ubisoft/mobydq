import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';

const SimpleButton = ({
  type,
  color,
  variant,
  disabled,
  label,
  touched, // eslint-disable-line
  onClick
}) => <Button type={type} disabled={disabled} variant={variant} color={color} onClick={onClick}>
  {label}
</Button>;

export default SimpleButton;

SimpleButton.propTypes = {
  'type': PropTypes.string.isRequired,
  'variant': PropTypes.string.isRequired,
  'disabled': PropTypes.bool.isRequired,
  'label': PropTypes.string.isRequired
};
