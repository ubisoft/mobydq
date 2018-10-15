import React from 'react';
import { Link } from 'react-router-dom';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import {ListTableCell} from './ListTableCell';

/**
 * Container component for TableRow Action Buttons

 * @param buttons a list of buttons
 * @param value an id of the row element
 * @param button.function a predefined button function (currently edit/delete).
 * #param button.parameter base_path for a predefined function or a custom function for a custom action
 *
 * Calls a Button component to render each button
 */
export const ListTableRowButtons = ({buttons, value}) => {

  return (
    <ListTableCell
      contents={
        buttons.map((button) => (
            _createButton(button, value)
        ), value)
      }
    />
  )
}

function _createButton(button, value) {
  switch(button.function) {
    case 'edit':
      return (
          <IconButton key={'edit_' + value} component={Link} to={button.parameter + '/edit/' + value} aria-label="Delete" color="primary">
            <EditIcon/>
          </IconButton>
      );
    default:
      return(
        <IconButton key={'delete_' + value} onClick={() => _delete(button.parameter, value)} aria-label="Delete" color="primary">
          <DeleteIcon/>
        </IconButton>
      );
  }

}

function _delete(repository, id) {
  alert('Delete using ' + repository + ' having id ' + id);
}
