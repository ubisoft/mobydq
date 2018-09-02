import React from 'react';
import { styles } from './../../styles/baseStyles'
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import { Query } from "react-apollo";
import gql from "graphql-tag";
import DataTable from '../Dashboard/DataTable'


class IndicatorGroupList extends React.Component {
  render() {
    const { classes } = this.props;
    const IndicatorGroupList = () => (
      <Query
        query={gql`
          {
            allIndicatorGroups {
              nodes {
                id
                name
                createdDate
                updatedDate
              }
            }
          }
        `}
      >
        {({ loading, error, data }) => {
          if (loading) return <p>Loading...</p>;
          if (error) return <p>Error :(</p>;

          return(
            <DataTable data={data.allIndicatorGroups.nodes}/>
          );
        }}
      </Query>
    );
    return (
      <React.Fragment>
        <div className={classes.appBarSpacer} />
        <Typography variant="display1" gutterBottom className={classes.chartContainer}>
          Indicator group
            <IndicatorGroupList/>
        </Typography>
      </React.Fragment>
     )
  }
}
export default withStyles(styles)(IndicatorGroupList);