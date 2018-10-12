import React from 'react';
import {ListTableCell} from './ListTableCell';
import SimpleButton from '@material-ui/core/Button';

/**
 * Container component for TableRow Action Buttons

 * @param buttons a lits of buttons
 * @param value an id of the row element
 *
 * Calls a Button component to render each button
 */
export const ListTableRowButtons = ({buttons, value}) => {
  return (
    <ListTableCell
      contents={
        buttons.map((button) => (
          <Button key={button.name} variant="outlined" value={value} className="btn btn-primary"
            onClick={button.function}>{button.name}</Button>
        ))
      }
    />
  )
}