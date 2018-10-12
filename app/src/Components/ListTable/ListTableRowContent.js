import React from 'react';
import DoneIcon from '@material-ui/icons/Done';
import ClearIcon from '@material-ui/icons/Clear';
import ListTableCell from './ListTableCell';

/**
 * Container component for TableRow Data Cells

 * @param buttons a lits of buttons
 * @param value an id of the row element
 *
 * Calls a SimpleButton component to render each button
 */
export const ListTableRowContent = ({rowData, rowColumns}) => {
  return rowColumns.map(function(column) {
    return (<ListTableCell key={rowData.id + '_' + column} contents={_buildCell(rowData[column])}/>)
  }, rowData);
}

function _buildCell(cellValue) {
  if(typeof(cellValue) === 'boolean') {
    if (cellValue) {
      return <DoneIcon color="primary"/>;
    }
    return <ClearIcon color="error"/>
  }
  return cellValue
}
