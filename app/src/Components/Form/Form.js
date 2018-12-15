import React from 'react';
import { Query, Mutation } from 'react-apollo';
import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';

const BaseForm = ({ title, FormComponent, ComponentRepository, afterSaveRoute, history, initialFieldValues, dropDownData }) => {
  const mutation = initialFieldValues === null ? ComponentRepository.insert() : ComponentRepository.update();
  const recordId = initialFieldValues === null ? null : initialFieldValues.id;
  return <Mutation
    mutation={mutation}
    onCompleted={() => {
      history.push(afterSaveRoute);
    }}
  >
    {(mutate, { loading, error }) => <React.Fragment>
      <div style={{ 'float': 'right', 'visibility': initialFieldValues === null ? 'hidden' : 'visible' }}>
        {
          _deleteMutation(
            ComponentRepository,
            recordId,
            () => {
              history.push(afterSaveRoute);
            }
          )
        }
      </div>
      <div style={{ 'marginLeft': '50px' }}>{title}</div>
      <FormComponent
        data={dropDownData}
        mutate={mutate}
        initialFieldValues={initialFieldValues}
      />
      {loading && <p>Loading...</p>}
      {error && <p>Error .. Please try again</p>}

    </React.Fragment>}
  </Mutation>;
};

function _deleteMutation(ComponentRepository, idToDelete, afterSave) {
  return (
    <Mutation
      mutation={ComponentRepository.delete()}
      variables={{ 'id': idToDelete }}
      onCompleted={afterSave}
    >
      { (deleteFunc, { loading, error }) => {
        const deleteMutationLoading = loading;
        const deleteMutationError = error;
        if (deleteMutationLoading) {
          return <p>Loading...</p>;
        }
        if (deleteMutationError) {
          return <p>Error...</p>;
        }
        return (
          <Button
            onClick={() => {
              deleteFunc();
            }}
            variant="contained">
            <DeleteIcon/> Delete
          </Button>
        );
      }}
    </Mutation>
  );
}

function withDropDownData(FormWithDropDown) {
  return function wrappedWithDropDownData(props) {
    return <Query query={props.ComponentRepository.getFormDropdownData()}>
      {({ loading, error, data }) => {
        if (typeof props.ComponentRepository.insert === 'undefined' || typeof props.ComponentRepository.getFormDropdownData === 'undefined') {
          throw new TypeError('Repository must implement insert and getFormDropdownData functions.');
        }
        if (loading) {
          return <p>Loading...</p>;
        }
        if (error) {
          return <p>Error :(</p>;
        }
        return <FormWithDropDown dropDownData={data} {...props} />;
      }}
    </Query>;
  };
}

export const EnhancedForm = withDropDownData(BaseForm);
