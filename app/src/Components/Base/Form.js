import React from 'react';
import { Query, Mutation } from 'react-apollo';


export const BaseForm = ({ title, FormComponent, ComponentRepository, afterSaveRoute, history, initialFieldValues}) => (
  <Query query={ComponentRepository.getFormDropdownData()}>
    {({ loading, error, data }) => {
      if (ComponentRepository.insert === undefined || ComponentRepository.getFormDropdownData === undefined) {
        throw new TypeError('Repository must implement insert and getFormDropdownData functions.')
      }
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;
      return (
        <Mutation mutation={ComponentRepository.insert()} onCompleted={() => { history.push(afterSaveRoute) }}>
          {(mutate, { loading, error }) => (
            <React.Fragment>
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



