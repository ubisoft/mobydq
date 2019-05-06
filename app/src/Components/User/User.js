import React from 'react';
import { Route } from 'react-router-dom';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import UserList from './UserList';
import EnhancedUserForm from './UserForm';

import { EnhancedForm } from './../Form/Form';
import { UserUpdateForm } from './UserUpdateForm';
import UserRepository from '../../repository/UserRepository';
import PrivateRoute from '../Base/PrivateRoute';

class User extends React.Component {
  render() {
    const { classes } = this.props;
    const { match } = this.props;
    return (
      <React.Fragment>
        <div className={classes.appBarSpacer} />
        <Typography variant="display1" gutterBottom className={classes.chartContainer}>
          <PrivateRoute
            permissions={['w_users']}
            path={`${match.url}/new`}
            component={
              (props) => <EnhancedForm ComponentRepository={UserRepository} FormComponent={EnhancedUserForm}
                                       afterSave={() => this.props.history.push('/user/')} title="Create User" initialFieldValues={null} {...props} />
            }
          />
          <PrivateRoute
            permissions={['w_users']}
            path={`${match.url}/edit/:id`}
            component={
              (props) => <UserUpdateForm afterSave={() => this.props.history.push('/user/')} {...props} />
            }
          />
          { /* Doesn't need to be private because the permission scope is already set in the content page */ }
          <Route
            exact
            path={match.url}
            render={() => <UserList refetch />}
          />
        </Typography>
      </React.Fragment>
    );
  }
}
export default withStyles(styles)(User);
