import React from 'react';

import { Query } from 'react-apollo';
import DataSourceRepository from '../../repository/DataSourceRepository';
import { GraphQLError } from './../Error/GraphQLError';

import NotFoundComponent from '../Error/NotFoundComponent';
import { EnhancedForm } from '../Form/Form';
import EnhancedDataSourceForm from './DataSourceForm';

export const DataSourceUpdateForm = ({ ...props }) => <Query query={DataSourceRepository.display()} variables={{ 'id': parseInt(props.match.params.id, 10) }}>
  {({ loading, error, data }) => {
    if (typeof DataSourceRepository.display !== 'function') {
      throw new TypeError('Repository must implement update function.');
    }
    if (loading) {
      return <p>Loading...</p>;
    }
    if (error) {
      return <GraphQLError error={error}/>;
    }
    return (
      data.dataSourceById === null
        ? <NotFoundComponent/>
        : <EnhancedForm ComponentRepository={DataSourceRepository} FormComponent={EnhancedDataSourceForm}
          afterSave={props.afterSave} title="Edit Data Source" initialFieldValues={data.dataSourceById} {...props}/>
    );
  }}
</Query>;
