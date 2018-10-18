import { Query } from 'react-apollo';
import React from 'react';

import IndicatorRepository from '../../repository/IndicatorRepository';
import NotFoundComponent from '../Error/NotFoundComponent';
import { BaseForm } from '../Base/Form';
import EnhancedIndicatorForm from './IndicatorForm';

export const IndicatorUpdateForm = ({ ...props }) => <Query query={IndicatorRepository.display()} variables={{ 'id': props.match.params.id }}>
  {({ loading, error, data }) => {
    if (typeof IndicatorRepository.display !== 'function') {
      throw new TypeError('Repository must implement update function.');
    }
    if (loading) {
      return <p>Loading...</p>;
    }
    if (error) {
      return <p>Error :(</p>;
    }
    return (
      data.indicatorGroupById === null
        ? <NotFoundComponent/>
        : <BaseForm ComponentRepository={IndicatorRepository} FormComponent={EnhancedIndicatorForm}
          afterSaveRoute="/indicator/" title="Edit Indicator" initialFieldValues={data.indicatorById} {...props}/>
    );
  }}
</Query>;
