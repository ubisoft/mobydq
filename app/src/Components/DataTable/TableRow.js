import React from 'react';
import PropTypes from 'prop-types';
import { styles } from '../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import TableCell from '@material-ui/core/TableCell';
import DoneIcon from '@material-ui/icons/Done';
import ClearIcon from '@material-ui/icons/Clear';
import TableRow from '@material-ui/core/TableRow';
import { TableRowButtons } from './TableRowButtons';
import Button from '@material-ui/core/Button';
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