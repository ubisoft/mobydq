import React from 'react';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';

import SimpleLineChart from '../../SimpleLineChart';
import SimpleTable from '../../SimpleTable';


class Dashboard extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <React.Fragment>
        <div className={classes.appBarSpacer} />
        <Typography variant="display1" gutterBottom className={classes.chartContainer}>
          Some awesome Ux lalalalalala
          ENV URL PARAM: {process.env.REACT_APP_GRAPHQL_API_URL}
        </Typography>
      </React.Fragment>
     )
  }
}

export default withStyles(styles)(Dashboard);