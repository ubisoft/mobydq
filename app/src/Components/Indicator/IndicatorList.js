import React from 'react';
import { Query } from 'react-apollo';
import IndicatorRepository from './../../repository/IndicatorRepository';
import ListTable from '../ListTable/ListTable';
import {LinkButton} from './../../Components/FormInput/SimpleButton';

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
            <LinkButton disabled={false} label="Create" type="Create" color='primary'
              variant='contained' to={'/indicator/new'}/>
          </div>
          <ListTable data={data.allIndicators.nodes}  buttons={[{'function': 'edit', 'parameter': '/indicator'}, {'function': 'delete', 'parameter': IndicatorRepository}]} />
        </div>
      );
    }}
  </Query>
);

export default IndicatorList;
