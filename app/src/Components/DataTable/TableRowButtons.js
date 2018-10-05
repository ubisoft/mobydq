import DoneIcon from "@material-ui/core/SvgIcon/SvgIcon";
import TableCell from "@material-ui/core/TableCell/TableCell";
import React from "react";

export const TableRowButtons = (buttons, value) => {
  return buttons.map((button) => (
    <TableCell>
      <button variant="outlined" value={value} className="btn btn-primary"
        onClick={button.function}>{button.name}</button>
    </TableCell>
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

function _renderButtons(buttons, value) {
  return buttons.map((button) => (
    <TableCell>
      <button variant="outlined" value={value} className="btn btn-primary"
        onClick={button.function}>{button.name}</button>
    </TableCell>
  ));
}