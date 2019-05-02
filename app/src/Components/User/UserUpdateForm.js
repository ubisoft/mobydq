import React from 'react';

import { Query } from 'react-apollo';
import UserRepository from '../../repository/UserRepository';
import { GraphQLError } from './../Error/GraphQLError';

import NotFoundComponent from '../Error/NotFoundComponent';

import { EnhancedForm } from '../Form/Form';
import EnhancedUserForm from './UserForm';

export const UserUpdateForm = ({ ...props }) => <Query query={UserRepository.display()} variables={{ 'id': parseInt(props.match.params.id, 10) }}>
  {({ loading, error, data }) => {
    if (typeof UserRepository.display !== 'function') {
      throw new TypeError('Repository must implement update function.');
    }
    if (loading) {
      return <GraphQLError error={error}/>;
    }
    if (error) {
      return <p>Error :(</p>;
    }
    return (
      data.UserById === null
        ? <NotFoundComponent/>
        : <EnhancedForm ComponentRepository={UserRepository} FormComponent={EnhancedUserForm}
          afterSave={props.afterSave} title="Edit User" initialFieldValues={data.userById} {...props}/>
    );
  }}
</Query>;
