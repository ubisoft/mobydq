import React from 'react';
import './../../styles/baseStyles';
import LinkButton from './../FormInput/LinkButton';

export const UnauthorizedError = () => <div style={{ 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center' }}>
  <div>
    <div style={{ 'textAlign': 'center' }}>
      Your session has expired
    </div>
    <div style={{ 'textAlign': 'center' }}>
      <LinkButton label="Re-login" type="Create" color="secondary" variant="contained" to={'/login'}/>
    </div>
  </div>
</div>;
