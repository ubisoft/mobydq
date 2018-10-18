import React from 'react';
import { Link } from 'react-router-dom';
import { Mutation } from 'react-apollo';


import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import { ListTableCell } from './ListTableCell';


/**
 * Container component for TableRow Action Buttons
 *
 * @param buttons a list of buttons
 * @param value an id of the row element
 * #param button.parameter base_path for a predefined function or a custom function for a custom action
 *
 * Calls a Button component to render each button
 */
export const ListTableRowButtons = ({ buttons, value }) => <ListTableCell
  contents={
    buttons.map((button) => _createButton(button, value)
      , value)
  }
/>;

function _createButton(button, value) {
  switch (button.function) {
  case 'edit':
    return (
      <IconButton key={`edit_${value}`} component={Link} to={`${button.parameter}/edit/${value}`} color="primary">
        <EditIcon/>
      </IconButton>
    );
  case 'delete':
    return (
      <Mutation
        key={`delete_${value}`}
        mutation={button.parameter.delete()}
        variables={{ 'id': value }}
        refetchQueries={[{ 'query': button.parameter.getListPage() }]}
      >
        { (deleteFunc, { loading, error }) => {
          if (loading) {
            return <p>Loading...</p>;
          }
          if (error) {
            return <p>Error...</p>;
          }
          return (
            <IconButton key={`delete_${value}`} onClick={() => {
              deleteFunc();
            }} color="primary">
              <DeleteIcon/>
            </IconButton>
          );
        }
        }
      </Mutation>
    );
  default:
    return <React.Fragment key={`none_${value}`} />;
  }
}
