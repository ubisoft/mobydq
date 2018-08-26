import React from 'react';
import { Query } from "react-apollo";
import gql from "graphql-tag";
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'

class IndicatorList extends React.Component {
  _parseResponse(indicatorNodes) {
    return indicatorNodes.map(({ id, name, description, executionOrder }) => (
      <TableRow>
        <TableCell>{id}</TableCell>
        <TableCell>{name}</TableCell>
        <TableCell>{description}</TableCell>
        <TableCell>{executionOrder}</TableCell>
      </TableRow>
    ));
  }

  render() {
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
            }

            }
          }
        `}
      >
        {({ loading, error, data }) => {
          if (loading) return <p>Loading...</p>;
          if (error) return <p>Error :(</p>;

          return(
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Id</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Execution Order</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                  {this._parseResponse(data.allIndicators.nodes)}
              </TableBody>
            </Table>
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