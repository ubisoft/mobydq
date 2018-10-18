import React from 'react';
import { Query, Mutation } from 'react-apollo';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';

export const BaseForm = ({ title, FormComponent, ComponentRepository, afterSaveRoute, history, initialFieldValues }) => <Query query={ComponentRepository.getFormDropdownData()}>
  {({ queryLoading, queryError, queryData }) => {
    if (typeof ComponentRepository.insert !== 'function' || typeof ComponentRepository.getFormDropdownData !== 'function') {
      throw new TypeError('Repository must implement insert and getFormDropdownData functions.');
    }
    const mutation = initialFieldValues === null ? ComponentRepository.insert() : ComponentRepository.update();
    if (queryLoading) {
      return <p>Loading...</p>;
    }
    if (queryError) {
      return <p>Error :(</p>;
    }
    return (
      <Mutation mutation={mutation} onCompleted={() => {
        history.push(afterSaveRoute);
      }}>
        {(mutate, { mutationLoading, mutationError }) => <React.Fragment>
          <div style={{ 'float': 'right', 'visibility': initialFieldValues === null ? 'hidden' : 'visible' }}>
            <Mutation
              mutation={ComponentRepository.delete()}
              variables={{ 'id': initialFieldValues === null ? null : initialFieldValues.id }}
              onCompleted={() => {
                history.push(afterSaveRoute);
              }}
            >
              { (deleteFunc, { deleteLoading, deleteError }) => {
                if (deleteLoading) {
                  return <p>Loading...</p>;
                }
                if (deleteError) {
                  return <p>Error...</p>;
                }
                return (
                  <IconButton onClick={() => {
                    deleteFunc();
                  }} color="primary">
                    <DeleteIcon/>
                  </IconButton>
                );
              }
              }
            </Mutation>
          </div>
          <div style={{ 'marginLeft': '60px' }}>{title}</div>
          <FormComponent
            data={queryData}
            mutate={mutate}
            initialFieldValues={initialFieldValues}
          />
          {mutationLoading && <p>Loading...</p>}
          {mutationError && <p>Error :( Please try again</p>}

        </React.Fragment>
        }
      </Mutation>
    );
  }}

</Query>;
