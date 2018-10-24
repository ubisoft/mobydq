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

class ListTableRowButtons extends React.Component {
  render() {
    return <ListTableCell contents={this.props.buttons.map((button) => this._createButton(button))}/>;
  }

  _createButton(button) {
    const recordId = this.props.value;

    switch (button.function) {
    case 'edit':
      return (
        <IconButton key={`edit_${recordId}`} component={Link} to={`${button.parameter}/edit/${recordId}`} color="primary">
          <EditIcon/>
        </IconButton>
      );
    case 'delete':
      const rowsPerPage = button.parameter.rowsPerPage;
      const page = button.parameter.page;
      const rowTotal = button.parameter.rowTotal;
      return (
        <Mutation
          key={`delete_${recordId}`}
          mutation={button.parameter.repository.delete()}
          variables={{ 'id': recordId }}
          refetchQueries={[{ 'query': button.parameter.repository.getListPage(), 'variables': { 'first': rowsPerPage, 'offset': rowsPerPage * page } }]}
          onCompleted={() => {
            // If deleting a row would make the page empty, jump to the previous row
            if (rowsPerPage * page === rowTotal - 1 && page > 0) {
              button.parameter.setPage(page - 1);
            }
          }}
        >
          { (deleteFunc, { loading, error }) => {
            if (loading) {
              return <p>Loading...</p>;
            }
            if (error) {
              return <p>Error...</p>;
            }
            return (
              <IconButton key={`delete_${recordId}`} onClick={() => {
                deleteFunc();
              }} color="primary">
                <DeleteIcon/>
              </IconButton>
            );
          }}
        </Mutation>
      );
    default:
      return <React.Fragment key={`none_${recordId}`} />;
    }
  }
}

export default ListTableRowButtons;
