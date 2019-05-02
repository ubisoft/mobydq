import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import SessionUser from '../../Authentication/SessionUser';
import UserRolePermissions from '../../Authentication/UserRolePermissions';

const PrivateRoute = ({ 'component': Component, ...parentProps }) => <Route {...parentProps} render={(props) => isAuthenticated(parentProps)
  ? <Component {...props} />
  : <Redirect to={{
    'pathname': '/login',
    'state': { 'from': props.location, 'message': 'You don\'t have access to this page.' }
  }} />
} />;

function isAuthenticated(props) {
  // Null = not logged in
  if (SessionUser.user) {
    const userPermissions = UserRolePermissions.getPermissionsObjectByRole(SessionUser.user.role);
    return props.permissions.every((permission) => userPermissions.permissions.includes(permission));
  }

  return false;
}

export function checkLoggedIn() {
  const cookieValue = getCookieValue('token');
  if (cookieValue) {
    const token = parseJwt(cookieValue);
    if (token === '') {
      return false;
    }
    return true;
  }
  return false;
}

export default PrivateRoute;
