import React from 'react';
import './../../styles/baseStyles';
import LinkButton from './../FormInput/LinkButton';

export const UnauthorisedError = () => <div style={{ 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center' }}>
  <div>
    <h4>Login expired</h4>
    <LinkButton disabled={false} label="Click here to re-login" type="Create" color="primary"
      variant="contained" to={'/login'}/>
  </div>
</div>;
