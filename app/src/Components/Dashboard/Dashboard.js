import React from 'react';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';


class Dashboard extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <React.Fragment>
        <div className={classes.appBarSpacer} />
        <Typography variant="display1" gutterBottom className={classes.chartContainer}>
          Documentation: <a href="https://mobydq.github.io">https://mobydq.github.io</a><br/>
          Flask API: <a href="/mobydq/api/doc">{process.env.REACT_APP_HOST_NAME}/mobydq/api/doc</a>
        </Typography>
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(Dashboard);
