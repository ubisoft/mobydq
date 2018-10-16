import React from 'react';
import { Query } from 'react-apollo';
import IndicatorRepository from './../../repository/IndicatorRepository';
import ListTable from '../ListTable/ListTable';
import RouterButton from './../../Components/FormInput/RouterButton';

const IndicatorList = (refetch) => (
  <Query
    query={IndicatorRepository.getListPage(1, 10)}
    fetchPolicy={refetch ? 'cache-and-network' : 'cache-first'}
  >
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;
      return (
        <div>
          <div style={{float: 'left', marginLeft: '60px'}}>
            Indicators
          </div>
          <div style={{ float: 'right' }}>
            <RouterButton targetLocation='/indicator/new' disabled={false} label="Create" variant='contained'/>
          </div>
          <ListTable data={data.allIndicators.nodes}  buttons={[{'name': 'edit', 'function': 'edit', 'parameter': '/indicator'}, {'name': 'delete', 'function': 'delete', 'parameter': 'IndicatorRepository'}]} />
        </div>
      );
    }}
  </Query>
);

export default IndicatorList;
