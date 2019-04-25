import React from 'react';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import ParameterList from './ParameterList';
import EnhancedParameterForm from './ParameterForm';
import ParameterRepository './../../../repository/ParameterRepository';
import { Route } from 'react-router-dom';

import { EnhancedForm } from './../Form/Form';
import { ParameterUpdateForm } from '../Parameter/ParameterUpdateForm';

class Parameter extends React.Component {
  render() {
    const { classes } = this.props;
    const { match } = this.props;
    return (
      <React.Fragment>
        <Typography variant="display1" gutterBottom className={classes.chartContainer}>
          <ParameterList this.props.parameters />
        </Typography>
      </React.Fragment>
    );
  }
}
export default withStyles(styles)(Parameter);
