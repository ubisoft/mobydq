import React from 'react';
import { Mutation } from 'react-apollo';
import { connect } from 'react-redux';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import { setAlertDialog } from '../../../actions/app';


class DeleteRowButton extends React.Component {
  confirmDelete = (func) => {
    this.props.setAlertDialog({
      'title': 'Delete',
      'description': 'Do you really want to delete this record?',
      'yesText': 'Yes',
      'noText': 'No',
      'onYes': func,
      'onNo': () => {}
    });
  }

  render() {
    const { rowsPerPage, page, rowTotal, sortColumn, repository, setPage, usePagination } = this.props.parameter;
    const { recordId } = this.props;
    return (
      <Mutation
        key={`delete_${recordId}`}
        mutation={repository.delete()}
        variables={{ 'id': recordId }}
        refetchQueries={usePagination && [{ 'query': repository.getListPage(), 'variables': { 'first': rowsPerPage, 'offset': rowsPerPage * page, 'orderBy': sortColumn } }]}
        onCompleted={() => {
          // If deleting a row would make the page empty, jump to the previous page
          if (usePagination === false) {
            window.location.reload();
          } else if (rowsPerPage * page === rowTotal - 1 && page > 0) {
            setPage(page - 1);
          }
        }}>
        {(deleteFunc, { loading, error }) => {
          if (loading) {
            return <p>Loading...</p>;
          }
          if (error) {
            return <p>Error...</p>;
          }
          return <IconButton
            key={`delete_${recordId}`}
            onClick={() => {
              this.confirmDelete(deleteFunc);
            }}
            color={'secondary'}
          >
            <DeleteIcon />
          </IconButton>;
        }}
      </Mutation>
    );
  }
}

const mapStateToProps = (state) => ({
  'alertDialog': state.alertDialog
});

const mapDispatchToProps = (dispatch) => ({
  'setAlertDialog': (alertDialog) => dispatch(setAlertDialog(alertDialog))
});


const VisibleDeleteRowButton = connect(mapStateToProps, mapDispatchToProps)(DeleteRowButton);

export default function createDeleteRowButton(button, recordId) {
  return <VisibleDeleteRowButton
    key={recordId}
    parameter={button.parameter}
    recordId={recordId}>
  </VisibleDeleteRowButton>;
}
