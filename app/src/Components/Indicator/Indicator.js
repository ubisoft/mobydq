import React from 'react';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import IndicatorList from './IndicatorList';
import EnhancedIndicatorForm from './IndicatorForm';
import IndicatorRepository from './../../repository/IndicatorRepository';
import { Route, withRouter } from 'react-router-dom';

import { EnhancedForm } from './../Form/Form';
import { IndicatorUpdateForm } from '../Indicator/IndicatorUpdateForm';

class Indicator extends React.Component {
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
              (props) => <EnhancedForm ComponentRepository={IndicatorRepository} FormComponent={EnhancedIndicatorForm}
                afterSave={() => this.props.history.push('/indicator/')} title="Create Indicator" initialFieldValues={null} {...props} />
            }
          />
          <Route
            path={`${match.url}/edit/:id`}
            component={
              (props) => <IndicatorUpdateForm afterSave={() => this.props.history.push('/indicator/')} {...props} />
            }
          />
          <Route
            exact
            path={match.url}
            render={() => <IndicatorList refetch />}
          />
        </Typography>
      </React.Fragment>
    );
  }
}
export default withRouter(withStyles(styles)(Indicator));
