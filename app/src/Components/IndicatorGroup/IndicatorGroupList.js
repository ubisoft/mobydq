import React from 'react';
import { styles } from './../../styles/baseStyles'
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';

class IndicatorGroupList extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <React.Fragment>
        <div className={classes.appBarSpacer} />
        <Typography variant="display1" gutterBottom className={classes.chartContainer}>
          Indicator group
        </Typography>
      </React.Fragment>
     )
  }
}
export default withStyles(styles)(IndicatorGroupList);