import React from 'react';
import { Query } from "react-apollo";
import gql from "graphql-tag";
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import DataTable from '../Dashboard/DataTable';
import SimpleForm from '../SimpleForm/SimpleForm';

const createMutation = `mutation create {
      createIndicator(input: {indicator: {executionOrder: 123, name: "a new name", description: "a fancy description", indicatorTypeId:1, indicatorGroupId:1}}) {
        indicator {
          id
          name
          description
        }
      }
    }`

const IndicatorForm = () => (
  <Query
    query={gql`
      {
        allIndicatorTypes {
          nodes {
            id
            name
          }
        }
        allIndicatorGroups {
          nodes {
            id
            name
          }
        }
      }
    `}
  >
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;
      return(
       <SimpleForm data={data}/>
      );
    }}
  </Query>
);

export default IndicatorForm;
