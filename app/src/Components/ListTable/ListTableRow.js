import React from 'react';
import PropTypes from 'prop-types';
import { styles } from '../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import TableRow from '@material-ui/core/TableRow';
import { ListTableRowButtons } from './ListTableRowButtons';
import Style from '../../index.css';
import { ListTableRowContent } from "./ListTableRowContent";

/**
 * Container component for a single row of the list table
 *
 * @param rowContent - a single row DTO
 * @param fowColumns - array of table column names (required to iterate the object)
 * @param (Optional) buttons - list of buttons to be shown in Action column
 *
 * Container calls for TableDataRowButtons and TableDataRowData container components
 */
export const ListTableRow = ({rowData, rowColumns, buttons}) => {
  return(
    <TableRow>
      <ListTableRowContent rowData={rowData} rowColumns={rowColumns}/>
      <ListTableRowButtons buttons={buttons} value={rowData.id}/>
    </TableRow>
  );
}

ListTableRow.defaultProps = {
  buttons: [],
};

ListTableRow.propTypes = {
  buttons: PropTypes.array,
  rowData: PropTypes.object.isRequired,
  rowColumns: PropTypes.array.isRequired
};