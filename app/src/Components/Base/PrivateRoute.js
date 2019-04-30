import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import SessionUser from '../../actions/Auth/SessionUser';
import UserRolePermissions from '../../actions/Auth/UserRolePermissions';

const PrivateRoute = ({ 'component': Component, ...parentProps }) => <Route {...parentProps} render={(props) => isAuthenticated(parentProps)
  ? <Component {...props} />
  : <Redirect to={{
    'pathname': '/login',
    'state': { 'from': props.location }
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

export default PrivateRoute;
