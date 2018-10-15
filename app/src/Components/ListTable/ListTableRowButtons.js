import React from 'react';
import { Link } from 'react-router-dom'
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import {ListTableCell} from './ListTableCell';
import RouterButton from './../../Components/FormInput/RouterButton';

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
            <EditIcon />
          </IconButton>
      );
      default:
        return(
          <IconButton key={'delete_' + value} onClick={() => _delete(button.parameter, value)} aria-label="Delete" color="primary">
            <DeleteIcon />
          </IconButton>
        );
  }

}

function _delete(repository, id) {
  alert('Delete using ' + repository + ' having id ' + id);
}
