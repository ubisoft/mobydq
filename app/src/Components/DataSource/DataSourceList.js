import React from 'react';
import { Query } from "react-apollo";
import DataSourceRepository  from './../../repository/DataSourceRepository';
import DataTable from '../Dashboard/DataTable';
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
          Data Source list
          <div style={{float: 'right'}}>
            <RouterButton targetLocation='/data-source/new' disabled={false} label="Add new data source"/>
          </div>
          <DataTable data={data.allDataSources.nodes}/>
        </div>
      );
    }}
  </Query>
);

export default DataSourceList;