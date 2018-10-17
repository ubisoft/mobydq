import React from 'react';
import { Query } from 'react-apollo';
import DataSourceRepository  from './../../repository/DataSourceRepository';
import ListTable from '../ListTable/ListTable';
import {LinkButton} from './../../Components/FormInput/SimpleButton';

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
            <LinkButton disabled={false} label="Create" type="Create" color='primary'
              variant='contained' to={'/data-source/new'}/>
          </div>
          <ListTable data={data.allDataSources.nodes}  buttons={[{'function': 'edit', 'parameter': '/data-source'}, {'function': 'delete', 'parameter': DataSourceRepository}]}/>
        </div>
      );
    }}
  </Query>
);

export default DataSourceList;
