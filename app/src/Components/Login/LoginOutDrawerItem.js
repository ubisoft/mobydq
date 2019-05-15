import React from 'react';
import { Link } from 'react-router-dom';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import SessionUser from '../../Authentication/SessionUser';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import LockIcon from '@material-ui/icons/Lock';
import DevLog from '../../DevLog';


export default class LoginOutDrawerItem extends React.Component {
  onClick() {
    if (SessionUser.user) {
      SessionUser.logOut();
      DevLog.info('Logging out user');
    }
    DevLog.info('redirect to log in');
  }

  /*
   * Todo remove the errormessage that the user doesn't have access to the login page when the user tried to access another page before.
   * This is a very uncritical feature but requires a lot of changes in the code and debugging.
   */

  render() {
    return (
      <ListItem button onClick={() => this.onClick()} component={Link} to="/login">
        <ListItemIcon>
          <LockIcon/>
        </ListItemIcon>
        <ListItemText primary={SessionUser.user ? 'Logout' : 'Login'}/>
      </ListItem>);
  }
}
