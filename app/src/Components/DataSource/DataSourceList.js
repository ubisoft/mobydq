import React from 'react';
import { Query } from 'react-apollo';
import DataSourceRepository  from './../../repository/DataSourceRepository';
import ListTable from '../ListTable/ListTable';
import RouterButton from './../../Components/FormInput/RouterButton';

const DataSourceList = (refetch) => (
  <Query
    query={DataSourceRepository.getListPage(1, 10)}
    fetchPolicy={refetch ? 'cache-and-network': 'cache-first'}
  >
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;
      return (
        <div>
          <div style={{float: 'left', marginLeft: '60px'}}>
            Data Sources
          </div>
          <div style={{float: 'right'}}>
            <RouterButton targetLocation='/data-source/new' disabled={false} label="Create" variant='contained'/>
          </div>
          <ListTable data={data.allDataSources.nodes}  buttons={[{'name': 'edit', 'function': 'edit', 'parameter': '/data-source'}, {'name': 'delete', 'parameter': 'DataSourceRepository'}]}/>
        </div>
      );
    }}
  </Query>
);

export default DataSourceList;
