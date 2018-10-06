import React from "react";
import DoneIcon from '@material-ui/icons/Done';
import ClearIcon from '@material-ui/icons/Clear';
import TableCell from "@material-ui/core/TableCell/TableCell";

export const TableRowData = ({rowData, rowColumns}) => {
  return rowColumns.map(function(column) {
    return (<TableCell key={rowData.id + '_' + column}>{_buildCell(rowData[column])}</TableCell>)
  }, rowData);
}

function _buildCell(cellValue) {
  if(typeof(cellValue) === "boolean") {
    if (cellValue) {
      return <DoneIcon color="primary"/>;
    }
    return <ClearIcon color="error"/>
  }
  return cellValue
}
