import React from 'react';
import { Route, withRouter } from 'react-router-dom';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import DataSourceList from './DataSourceList';
import EnhancedDataSourceForm from './DataSourceForm';
import DataSourceRepository from './../../repository/DataSourceRepository';

import { EnhancedForm } from './../Form/Form';
import { DataSourceUpdateForm } from './DataSourceUpdateForm';

class DataSource extends React.Component {
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
              (props) => <EnhancedForm ComponentRepository={DataSourceRepository} FormComponent={EnhancedDataSourceForm}
                afterSave={() => this.props.history.push('/data-source/')} title="Create Data Source" initialFieldValues={null} {...props} />
            }
          />
          <Route
            path={`${match.url}/edit/:id`}
            component={
              (props) => <DataSourceUpdateForm {...props} />
            }
          />
          <Route
            exact
            path={match.url}
            render={() => <DataSourceList refetch />}
          />
        </Typography>
      </React.Fragment>
    );
  }
}
export default withRouter(withStyles(styles)(DataSource));
