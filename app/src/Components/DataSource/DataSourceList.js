import React from 'react';
import { styles } from './../../styles/baseStyles'
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';

class DataSourceList extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <React.Fragment>
        <div className={classes.appBarSpacer} />
        <Typography variant="display1" gutterBottom className={classes.chartContainer}>
          Data source list
        </Typography>
      </React.Fragment>
     )
  }
}
export default withStyles(styles)(DataSourceList);