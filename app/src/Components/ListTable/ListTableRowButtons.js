import React from "react";
import {ListTableCell} from "./ListTableCell";

/**
 * Container component for TableRow Action Buttons

 * @param buttons a lits of buttons
 * @param value an id of the row element
 *
 * Calls a SimpleButton component to render each button
 */
export const ListTableRowButtons = ({buttons, value}) => {
  return (
    <ListTableCell
      contents={
        buttons.map((button) => (
          <button key={button.name} variant="outlined" value={value} className="btn btn-primary"
            onClick={button.function}>{button.name}</button>
        ))
      }
    />
  )
}