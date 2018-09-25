import React from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import RouterButton from './../../Components/FormInput/RouterButton';
import IndicatorList from './IndicatorList';
import EnhancedIndicatorForm from './IndicatorForm';
import IndicatorRepository from './../../repository/IndicatorRepository';

import BaseForm from './../Base/Form'

class Indicator extends React.Component {
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
              (props) => ( <BaseForm ComponentRepository={IndicatorRepository} FormComponent={EnhancedIndicatorForm}
                  afterSaveRoute='/indicator/' title='Add New Indicator' {...props} /> )
            }
          />
          <Route
            exact
            path={match.url}
            render={() => <IndicatorList refetch />}
          />
        </Typography>
      </React.Fragment>
    )
  }
}
export default withStyles(styles)(Indicator);