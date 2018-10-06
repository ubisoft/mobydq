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
        <TableRowData rowData={this.props.rowContent} rowColumns={this.props.rowColumns}/>
        <TableRowButtons buttons={this.props.buttons} value={this.props.rowContent[0]}/>
      </TableRow>
    );
  }
}

export default withStyles(styles)(DataTableRow);

DataTableRow.defaultProps = {
  buttons: [],
};

DataTableRow.propTypes = {
  buttons: PropTypes.array,
  rowContent: PropTypes.object.isRequired,
  rowColumns: PropTypes.array.isRequired
};