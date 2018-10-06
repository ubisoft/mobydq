import React from 'react';
import PropTypes from 'prop-types';
import { styles } from '../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import TableRow from '@material-ui/core/TableRow';
import { TableRowButtons } from './TableRowButtons';
import Style from '../../index.css';
import { TableRowData } from "./TableRowData";


class DataTableRow extends React.Component
{
  render() {
    return(
      <TableRow>
        <TableRowData rowData={this.props.rowData}/>
        <TableRowButtons buttons={this.props.buttons} value={this.props.rowData[0]}/>
      </TableRow>
    );
  }
}

export default withStyles(styles)(DataTableRow);

TableRow.defaultProps = {
  rowData: [],
  buttons: [],
};

TableRow.propTypes = {
  buttons: PropTypes.array,
  rowData: PropTypes.array.isRequired
};