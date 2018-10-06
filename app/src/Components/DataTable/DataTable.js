import React from 'react';
import { styles } from '../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableHead from '@material-ui/core/TableHead';
import TableHeader from './TableHeader';
import DataTableBody from './TableBody';

class DataTable extends React.Component {
  _buildTableFieldNames() {
    var tableFieldNames = Object.keys(this.props.data[0]);
    //remove redundant element
    tableFieldNames.pop();
    return tableFieldNames
  }

  _buildTableRowData() {
      return this.props.data.map((row) =>  {
        var rowArray = Object.values(row);
        // delete row.__typename;
        //remove __typename value
        rowArray.pop()
        return rowArray;
      })
  }

  render() {
    //check if correct data prop is passed, otherwise render empty.
    if (this.props.data === null || this.props.data.length === 0 || this.props.data.constructor !== Array) {
      return (<React.Fragment/>);
    }

    let headerNames = this._buildTableFieldNames();
    let content = this._buildTableRowData();
    return (
      <Table>
        <TableHead>
          <TableHeader headerNames={headerNames}/>
        </TableHead>
        <TableBody>
          <DataTableBody buttons={this.props.buttons} content={content} />
        </TableBody>
      </Table>
    );
  }
}

export default withStyles(styles)(DataTable);

DataTable.propTypes = {
  data: PropTypes.array.isRequired,
};

DataTable.defaultProps = {
  buttons: [],
};