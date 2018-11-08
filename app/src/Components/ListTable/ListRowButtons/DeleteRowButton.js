import React from 'react';
import { Mutation } from 'react-apollo';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';


export default function createDeleteRowButton(button, recordId) {
  const { rowsPerPage, page, rowTotal } = button.parameter;
  return (
    <Mutation
      key={`delete_${recordId}`}
      mutation={button.parameter.repository.delete()}
      variables={{ 'id': recordId }}
      refetchQueries={[{ 'query': button.parameter.repository.getListPage(), 'variables': { 'first': rowsPerPage, 'offset': rowsPerPage * page } }]}
      onCompleted={() => {
        // If deleting a row would make the page empty, jump to the previous page
        if (rowsPerPage * page === rowTotal - 1 && page > 0) {
          button.parameter.setPage(page - 1);
        }
      }}>
      {(deleteFunc, { loading, error }) => {
        if (loading) {
          return <p>Loading...</p>;
        }
        if (error) {
          return <p>Error...</p>;
        }
        return (
          <IconButton key={`delete_${recordId}`} onClick={() => {deleteFunc();}} color="secondary">
            <DeleteIcon />
          </IconButton>
        );
      }}
    </Mutation>
  );
}
