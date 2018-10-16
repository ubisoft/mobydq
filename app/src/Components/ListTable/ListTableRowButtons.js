import React from 'react';
import { Link, Redirect } from 'react-router-dom';
import { Mutation } from 'react-apollo';


import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import {ListTableCell} from './ListTableCell';


/**
 * Container component for TableRow Action Buttons

 * @param buttons a list of buttons
 * @param value an id of the row element
 * #param button.parameter base_path for a predefined function or a custom function for a custom action
 *
 * Calls a Button component to render each button
 */
export const ListTableRowButtons = ({buttons, value, history}) => {

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
  switch(button.name) {
    case 'edit':
      return (
          <IconButton key={'edit_' + value} component={Link} to={button.parameter + '/edit/' + value} aria-label="Delete" color="primary">
            <EditIcon/>
          </IconButton>
      );
    case 'delete':
      return(
      <div key={'delete_' + value}>
        <Mutation mutation={button.parameter.delete()} variables={{id: 'value'}} onCompleted={() => {null} }>
        { (deleteFunc, { loading, error, data }) => {
         if (loading) return (<p>Loading...</p>);
         if (error) return (<p>Loading...</p>);
         return(
           <IconButton key={'delete_' + value} onClick={() => {deleteFunc()}} aria-label="Delete" color="primary">
            <DeleteIcon/>
          </IconButton>
          )}
        }
        </Mutation>
      </div>
      );
    default:
      return <React.Fragment/>
  }

}
