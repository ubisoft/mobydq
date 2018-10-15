import React from 'react';
import { Route } from 'react-router-dom';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import IndicatorGroupList from './IndicatorGroupList';
import EnhancedIndicatorGroupForm from './IndicatorGroupForm';
import IndicatorGroupRepository from './../../repository/IndicatorGroupRepository';

import { BaseForm } from './../Base/Form'
import { IndicatorGroupUpdateForm } from './IndicatorGroupUpdateForm';

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
                  afterSaveRoute='/indicator-group/' title='Create Indicator Group'  initialFieldValues={null} {...props} /> )
            }
          />
          <Route
            path={`${match.url}/edit/:id`}
            component={
              (props) => ( <IndicatorGroupUpdateForm {...props} /> )
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
