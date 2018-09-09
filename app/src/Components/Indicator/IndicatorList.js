import React from 'react';
import { Query } from "react-apollo";
import IndicatorRepository  from './../../repository/IndicatorRepository';
import gql from "graphql-tag";
import DataTable from '../Dashboard/DataTable';
import RouterButton from './../../Components/FormInput/RouterButton';
//allIndicators(first:2, offset: 1) {

const IndicatorList = () => (

  <Query
    query={IndicatorRepository.getIndicatorListByPage(100, 0)}
  >
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;
      return(
        <div>
          Indicator list
          <RouterButton targetLocation='/indicators/new' disabled={false} label="Add new indicator"/>
          <RouterButton targetLocation='back' disabled={false} label="Indicator List"/>
          <DataTable data={data.allIndicators.nodes}/>
        </div>
      );
    }}
  </Query>
);

export default IndicatorList;