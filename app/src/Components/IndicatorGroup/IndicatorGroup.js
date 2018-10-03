import React from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import RouterButton from './../../Components/FormInput/RouterButton';
import IndicatorGroupList from './IndicatorGroupList';
import EnhancedIndicatorGroupForm from './IndicatorGroupForm';
import IndicatorGroupRepository from './../../repository/IndicatorGroupRepository';

import BaseForm from './../Base/Form'

class IndicatorGroup extends React.Component {
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
              (props) => ( <BaseForm ComponentRepository={IndicatorGroupRepository} FormComponent={EnhancedIndicatorGroupForm}
                  afterSaveRoute='/indicator-group/' title='Add New Indicator Group' {...props} /> )
            }
          />
          <Route
            exact
            path={match.url}
            render={() => <IndicatorGroupList refetch />}
          />
        </Typography>
      </React.Fragment>
    )
  }
}
export default withStyles(styles)(IndicatorGroup);