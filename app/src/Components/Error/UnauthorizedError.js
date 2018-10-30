import React from 'react';
import './../../styles/baseStyles';
import LinkButton from './../FormInput/LinkButton';

export const UnauthorizedError = () => <div style={{ 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center' }}>
  <div>
    <h4>Login expired</h4>
    <LinkButton label="Click here to re-login" type="Create" color="primary"
      variant="contained" to={'/login'}/>
  </div>
</div>;
