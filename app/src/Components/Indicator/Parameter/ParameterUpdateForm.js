import React from 'react';

import { Query } from 'react-apollo';
import ParameterRepository from '../../../repository/ParameterRepository';
import { GraphQLError } from './../../Error/GraphQLError';

import NotFoundComponent from '../../Error/NotFoundComponent';

import { EnhancedForm } from '../../Form/Form';
import EnhancedParameterForm from './ParameterForm';

export const ParameterUpdateForm = ({ ...props }) => <Query query={ParameterRepository.display()} variables={{ 'id': props.id }}>
  {({ loading, error, data }) => {
    if (typeof ParameterRepository.display !== 'function') {
      throw new TypeError('Repository must implement update function.');
    }
    if (loading) {
      return <p>Loading...</p>;
    }
    if (error) {
      return <GraphQLError error={error}/>;
    }
    return (
      data.parameterGroupById === null
        ? <NotFoundComponent/>
        : <EnhancedForm ComponentRepository={ParameterRepository} FormComponent={EnhancedParameterForm}
          afterSave={props.afterSave} title="Edit Parameter" initialFieldValues={data.parameterById} {...props}/>
    );
  }}
</Query>;
