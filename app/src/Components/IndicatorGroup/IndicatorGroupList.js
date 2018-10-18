import React from 'react';
import { Query } from 'react-apollo';
import IndicatorGroupRepository from './../../repository/IndicatorGroupRepository';
import ListTable from '../ListTable/ListTable';
import LinkButton from './../../Components/FormInput/LinkButton';

const IndicatorGroupList = (refetch) => <Query
  query={IndicatorGroupRepository.getListPage(1, 10)}
  fetchPolicy={refetch ? 'cache-and-network' : 'cache-first'}
>
  {({ loading, error, data }) => {
    if (loading) {
      return <p>Loading...</p>;
    }
    if (error) {
      return <p>Error :(</p>;
    }
    return (
      <div>
        <div style={{ 'float': 'left', 'marginLeft': '60px' }}>
            Indicator Groups
        </div>
        <div style={{ 'float': 'right' }}>
          <LinkButton disabled={false} label="Create" type="Create" color="primary"
            variant="contained" to={'/indicator-group/new'}/>
        </div>
        <ListTable data={data.allIndicatorGroups.nodes} buttons={[{ 'function': 'edit', 'parameter': '/indicator-group' }, { 'function': 'delete', 'parameter': IndicatorGroupRepository }]}/>
      </div>
    );
  }}
</Query>;
export default IndicatorGroupList;
