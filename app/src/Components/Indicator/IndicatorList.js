import React from 'react';
import { Query } from "react-apollo";
import gql from "graphql-tag";
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import DataTable from '../Dashboard/DataTable'

class IndicatorList extends React.Component {
  render() {
      console.log(process.env);
    const { classes } = this.props;
    const IndicatorList = () => (
      <Query
        query={gql`
          {
            allIndicators(first:2, offset: 1) {
              nodes{
                id
                name
                description
                executionOrder
                flagActive
                createdDate
                updatedDate
                indicatorTypeId
              } 
            }
          }
        `}
      >
        {({ loading, error, data }) => {
          if (loading) return <p>Loading...</p>;
          if (error) return <p>Error :(</p>;

          return(
            <DataTable data={data.allIndicators.nodes}/>
          );
        }}
      </Query>
    );
    return (
      <React.Fragment>
        <div className={classes.appBarSpacer} />
        <Typography variant="display1" gutterBottom className={classes.chartContainer}>
          Indicator list
            <IndicatorList/>
        </Typography>
      </React.Fragment>
     )
  }
}
export default withStyles(styles)(IndicatorList);