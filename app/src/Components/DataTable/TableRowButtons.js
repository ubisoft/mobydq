import React from "react";
import TableCell from "@material-ui/core/TableCell/TableCell";

export const TableRowButtons = ({buttons, value}) => {
  return (
    <TableCell>
      {
        buttons.map((button) => (
          <button key={button.name} variant="outlined" value={value} className="btn btn-primary"
            onClick={button.function}>{button.name}</button>
        ))
      }
    </TableCell>
  )
}