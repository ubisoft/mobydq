import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRoute = ({ 'component': Component, ...parentProps }) => <Route {...parentProps} render={(props) => isAuthenticated(parentProps)
  ? <Component {...props} />
  : <Redirect to={{
    'pathname': '/login',
    'state': { 'from': props.location }
  }} />
} />;
function isAuthenticated(props) {
  const cookieValue = getCookieValue('token');
  if (cookieValue) {
    const token = parseJwt(cookieValue);

    return props.permissions.every((permission) => token.role.includes(permission));
  }
  return false;
}

function parseJwt(token) {
  const [, base64Token] = token.split('.');
  const base64 = base64Token.replace('-', '+').replace('_', '/');
  return JSON.parse(window.atob(base64));
}

// TODO Re-use with Root.js
function getCookieValue(key) {
  const valueMatch = document.cookie.match(`(^|;)\\s*${key}\\s*=\\s*([^;]+)`);
  return valueMatch ? valueMatch.pop() : '';
}

export default PrivateRoute;
