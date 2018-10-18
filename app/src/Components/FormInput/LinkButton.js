import React from 'react';
import Button from '@material-ui/core/Button';

import { Link } from 'react-router-dom';

const LinkButton = ({
  type,
  color,
  variant,
  disabled,
  label,
  touched, // eslint-disable-line
  to
}) => <Button type={type} component={Link} to={to} disabled={disabled} variant={variant} color={color}>
  {label}
</Button>;

export default LinkButton;
