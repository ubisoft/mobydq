import React from 'react';
import { Query } from "react-apollo";
import gql from "graphql-tag";
import DataTable from '../Dashboard/DataTable'
import RouterButton from './../../Components/FormInput/RouterButton'

const IndicatorList = () => (
  <Query
    query={gql`
      {
        allIndicators(first:2, offset: 1) {
          nodes{
            id
            name
            description
            executionOrder
            flagActive
            createdDate
            updatedDate
            indicatorTypeId
          }
        }
      }
    `}
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