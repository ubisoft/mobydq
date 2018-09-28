import React from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import RouterButton from './../../Components/FormInput/RouterButton';
import DataSourceList from './DataSourceList';
import EnhancedDataSourceForm from './DataSourceForm';
import DataSourceRepository from './../../repository/DataSourceRepository';

import BaseForm from './../Base/Form';

class DataSource extends React.Component {
  render() {
    const { classes } = this.props;
    const { match } = this.props;
    return (
      <React.Fragment>
        <div className={classes.appBarSpacer} />
        <Typography variant='display1' gutterBottom className={classes.chartContainer}>
          <Route
            path={`${match.url}/new`}
            component={
              (props) => ( <BaseForm ComponentRepository={DataSourceRepository} FormComponent={EnhancedDataSourceForm}
                  afterSaveRoute='/data-source/' title='Add New Data Source' {...props} /> )
            }
          />
          <Route
            exact
            path={match.url}
            render={() => <DataSourceList refetch />}
          />
        </Typography>
      </React.Fragment>
    )
  }
}
export default withStyles(styles)(DataSource);