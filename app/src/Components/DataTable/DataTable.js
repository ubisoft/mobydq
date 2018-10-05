import React from 'react';
import { styles } from '../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import DoneIcon from '@material-ui/icons/Done';
import ClearIcon from '@material-ui/icons/Clear';
import TableHeader from './TableHeader';
import DataTableBody from './TableBody';

class DataTable extends React.Component {
  _buildCell(cellName, cellValue) {
    if (cellValue === true) {
      cellValue = <DoneIcon color="primary"/>;
    }
    if (cellValue === false) {
      cellValue = <ClearIcon color="error"/>
    }
    return (
      <TableCell key={cellName}>{cellValue}</TableCell>
    )
  }

  _buildTable(fieldNames) {
    return this.props.data.map((row) => (
      <TableRow key={row['id']}>
        {fieldNames.map((fieldName) => (this._buildCell(fieldName, row[fieldName])))}
      </TableRow>
    ));
  }

  render() {
    //check if correct data prop is passed, otherwise render empty.
    if (this.props.data === null || this.props.data.length === 0 || this.props.data.constructor !== Array) {
      return (<React.Fragment/>)
    }

    let tableFieldNames = Object.keys(this.props.data[0]);
    //remove redundant element
    tableFieldNames.pop();

    return (
      <Table>
        <TableHead>
          <TableHeader headerNames={tableFieldNames}/>
        </TableHead>
        <TableBody>
          <DataTableBody buttons={this.props.buttons} tableContent={Object.values(this.props.data)} />
        </TableBody>
      </Table>
    )
  }
}

export default withStyles(styles)(DataTable);

DataTable.propTypes = {
  data: PropTypes.array.isRequired,
};