import React from 'react';

import { Query } from 'react-apollo';
import IndicatorGroupRepository from '../../repository/IndicatorGroupRepository';
import { GraphQLError } from './../Error/GraphQLError';

import NotFoundComponent from '../Error/NotFoundComponent';

import { EnhancedForm } from '../Form/Form';
import EnhancedIndicatorGroupForm from './IndicatorGroupForm';

export const IndicatorGroupUpdateForm = ({ ...props }) => <Query query={IndicatorGroupRepository.display()} variables={{ 'id': parseInt(props.match.params.id, 10) }}>
  {({ loading, error, data }) => {
    if (typeof IndicatorGroupRepository.display !== 'function') {
      throw new TypeError('Repository must implement update function.');
    }
    if (loading) {
      return <GraphQLError error={error}/>;
    }
    if (error) {
      return <p>Error :(</p>;
    }
    return (
      data.indicatorGroupById === null
        ? <NotFoundComponent/>
        : <EnhancedForm ComponentRepository={IndicatorGroupRepository} FormComponent={EnhancedIndicatorGroupForm}
          afterSaveRoute="/indicator-group/" title="Edit Indicator Group" initialFieldValues={data.indicatorGroupById} {...props}/>
    );
  }}
</Query>;
