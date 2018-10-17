import React from 'react';
import { Query, Mutation } from 'react-apollo';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';

export const BaseForm = ({ title, FormComponent, ComponentRepository, afterSaveRoute, history, initialFieldValues}) => (
  <Query query={ComponentRepository.getFormDropdownData()}>
    {({ loading, error, data }) => {
      if (ComponentRepository.insert === undefined || ComponentRepository.getFormDropdownData === undefined) {
        throw new TypeError('Repository must implement insert and getFormDropdownData functions.')
      }
      let mutation = initialFieldValues === null ? ComponentRepository.insert() : ComponentRepository.update();
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;
      return (
        <Mutation mutation={mutation} onCompleted={() => { history.push(afterSaveRoute) }}>
          {(mutate, { loading, error }) => (
            <React.Fragment>
              <div style={{float: 'right', visibility: initialFieldValues !== null ? 'visible' : 'hidden'}}>
                <Mutation
                  mutation={ComponentRepository.delete()}
                  variables={{id: initialFieldValues !== null ? initialFieldValues.id : null}}
                  onCompleted={() => { history.push(afterSaveRoute) }}
                >
                  { (deleteFunc, { loading, error }) => {
                    if (loading) return (<p>Loading...</p>);
                    if (error) return (<p>Error...</p>);
                    return(
                      <IconButton onClick={() => {deleteFunc()}} aria-label="Delete" color="primary">
                        <DeleteIcon/>
                      </IconButton>
                      )
                    }
                  }
                </Mutation>
              </div>
              <div style={{ marginLeft: '60px' }}>{title}</div>
              <FormComponent
                data={data}
                mutate={mutate}
                initialFieldValues={initialFieldValues}
              />
              {loading && <p>Loading...</p>}
              {error && <p>Error :( Please try again</p>}

            </React.Fragment>
          )}
        </Mutation>
      );
    }}

  </Query>
);



