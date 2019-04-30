import React from 'react';

import { Query } from 'react-apollo';
import IndicatorRepository from '../../repository/IndicatorRepository';
import { GraphQLError } from './../Error/GraphQLError';

import NotFoundComponent from '../Error/NotFoundComponent';

import { EnhancedForm } from '../Form/Form';
import EnhancedIndicatorForm from './IndicatorForm';

import ParameterList from './Parameter/ParameterList';

export const IndicatorUpdateForm = ({ ...props }) => <Query query={IndicatorRepository.display()} variables={{ 'id': parseInt(props.match.params.id, 10) }}>
  {({ loading, error, data }) => {
    if (typeof IndicatorRepository.display !== 'function') {
      throw new TypeError('Repository must implement update function.');
    }
    if (loading) {
      return <p>Loading...</p>;
    }
    if (error) {
      return <GraphQLError error={error}/>;
    }
    return (
      data.indicatorGroupById === null
        ? <NotFoundComponent/>
        : <div>
          <EnhancedForm ComponentRepository={IndicatorRepository} FormComponent={EnhancedIndicatorForm}
              afterSave={props.afterSave} title="Edit Indicator" initialFieldValues={data.indicatorById} {...props}/>
          <ParameterList data={data.indicatorById.parametersByIndicatorId.nodes} indicatorId={data.indicatorById.id}/>
        </div>
    );
  }}
</Query>;
