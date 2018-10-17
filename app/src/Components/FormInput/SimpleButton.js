import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';

import { Link } from 'react-router-dom';

export const SimpleButton = ({
  type,
  color,
  variant,
  disabled,
  label,
  touched, // eslint-disable-line
  onClick
}) => {
  return (
    <Button type={type} disabled={disabled} variant={variant} color={color} onClick={onClick}>
      {label}
    </Button>
  )
}

export const LinkButton = ({
  type,
  color,
  variant,
  disabled,
  label,
  touched, // eslint-disable-line
  to
}) => {
  return (
    <Button type={type} component={Link} to={to} disabled={disabled} variant={variant} color={color}>
      {label}
    </Button>
  )
}

export default SimpleButton;

SimpleButton.propTypes = {
  type: PropTypes.string.isRequired,
  variant: PropTypes.string.isRequired,
  disabled: PropTypes.bool.isRequired,
  label: PropTypes.string.isRequired,
};