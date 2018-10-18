import { Query } from 'react-apollo';
import React from 'react';

import DataSourceRepository from '../../repository/DataSourceRepository';
import NotFoundComponent from '../Error/NotFoundComponent';
import { BaseForm } from '../Base/Form';
import EnhancedDataSourceForm from './DataSourceForm';

export const DataSourceUpdateForm = ({ ...props }) => <Query query={DataSourceRepository.display()} variables={{ 'id': props.match.params.id }}>
  {({ loading, error, data }) => {
    if (typeof DataSourceRepository.display !== 'function') {
      throw new TypeError('Repository must implement update function.');
    }
    if (loading) {
      return <p>Loading...</p>;
    }
    if (error) {
      return <p>Error :(</p>;
    }
    return (
      data.dataSourceById === null
        ? <NotFoundComponent/>
        : <BaseForm ComponentRepository={DataSourceRepository} FormComponent={EnhancedDataSourceForm}
          afterSaveRoute="/data-source/" title="Edit Data Source" initialFieldValues={data.dataSourceById} {...props}/>
    );
  }}
</Query>;
