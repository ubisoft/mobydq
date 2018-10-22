import React from 'react';
import { Query, Mutation } from 'react-apollo';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';

export const BaseForm = ({ title, FormComponent, ComponentRepository, afterSaveRoute, history, initialFieldValues}) => (
  <Query query={ComponentRepository.getFormDropdownData()}>
    {({ loading, error, data }) => {
      let queryLoading = loading;
      let queryError = error;
      let queryData = data;
      if (ComponentRepository.insert === undefined || ComponentRepository.getFormDropdownData === undefined) {
        throw new TypeError('Repository must implement insert and getFormDropdownData functions.')
      }
      let mutation = initialFieldValues === null ? ComponentRepository.insert() : ComponentRepository.update();
      let recordId = initialFieldValues !== null ? initialFieldValues.id : null;
      if (queryLoading) return <p>Loading...</p>;
      if (queryError) return <p>Error :(</p>;
      return (
        <Mutation mutation={mutation} onCompleted={() => { history.push(afterSaveRoute) }}>
          {(mutate, { loading, error }) => (
            <React.Fragment>
              <div style={{float: 'right', visibility: initialFieldValues !== null ? 'visible' : 'hidden'}}>
                {_deleteMutation(ComponentRepository, recordId, history, afterSaveRoute)}
              </div>
              <div style={{ marginLeft: '60px' }}>{title}</div>
              <FormComponent
                data={queryData}
                mutate={mutate}
                initialFieldValues={initialFieldValues}
              />
              {loading && <p>Loading...</p>}
              {error && <p>Error .. Please try again</p>}

            </React.Fragment>
          )}
        </Mutation>
      );
    }}

  </Query>
);

function _deleteMutation(ComponentRepository, idToDelete, history, afterSaveRoute) {
  return (
    <Mutation
      mutation={ComponentRepository.delete()}
      variables={{id: idToDelete}}
      onCompleted={() => { history.push(afterSaveRoute) }}
    >
      { (deleteFunc, { loading, error }) => {
        let deleteMutationLoading = loading;
        let deleteMutationError = error;
        if (deleteMutationLoading) return (<p>Loading...</p>);
        if (deleteMutationError) return (<p>Error...</p>);
        return(
          <IconButton onClick={() => {deleteFunc()}} color="primary">
            <DeleteIcon/>
          </IconButton>
          )
        }
      }
    </Mutation>
  )
}
