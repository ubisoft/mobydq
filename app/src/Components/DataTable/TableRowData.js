import React from "react";
import DoneIcon from "@material-ui/core/SvgIcon/SvgIcon";
import TableCell from "@material-ui/core/TableCell/TableCell";

export const TableRowData = (rowData) => {
  return rowData.map((value) => (
    <TableCell key={value}>{value} {this._isFlagActive(value)}</TableCell>
  ));
}

function _isFlagActive(flag) {
  if(typeof(flag) === "boolean") {
    if (flag) {
      return <DoneIcon color="primary"/>;
    }
    return <ClearIcon color="error"/>
  }
}