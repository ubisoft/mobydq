import React from 'react';
import { Route } from 'react-router-dom';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import UserGroupList from './UserGroupList';
import EnhancedUserGroupForm from './UserGroupForm';
import UserGroupRepository from './../../repository/UserGroupRepository';

import { EnhancedForm } from './../Form/Form';
import { UserGroupUpdateForm } from './UserGroupUpdateForm';

class UserGroup extends React.Component {
  render() {
    const { classes } = this.props;
    const { match } = this.props;
    return (
      <React.Fragment>
        <div className={classes.appBarSpacer} />
        <Typography variant="display1" gutterBottom className={classes.chartContainer}>
          <Route
            path={`${match.url}/new`}
            component={
              (props) => <EnhancedForm ComponentRepository={UserGroupRepository} FormComponent={EnhancedUserGroupForm}
                afterSave={() => this.props.history.push('/user-group/')} title="Create User Group" initialFieldValues={null} {...props} />
            }
          />
          <Route
            path={`${match.url}/edit/:id`}
            component={
              (props) => <UserGroupUpdateForm afterSave={() => this.props.history.push('/user-group/')} {...props} />
            }
          />
          <Route
            exact
            path={match.url}
            render={() => <UserGroupList refetch />}
          />
        </Typography>
      </React.Fragment>
    );
  }
}
export default withStyles(styles)(UserGroup);
