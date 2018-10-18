import { Query } from 'react-apollo';
import React from 'react';

import IndicatorGroupRepository from '../../repository/IndicatorGroupRepository';
import NotFoundComponent from '../Error/NotFoundComponent';
import { BaseForm } from '../Base/Form';
import EnhancedIndicatorGroupForm from './IndicatorGroupForm';

export const IndicatorGroupUpdateForm = ({ ...props }) => <Query query={IndicatorGroupRepository.display()} variables={{ 'id': props.match.params.id }}>
  {({ loading, error, data }) => {
    if (typeof IndicatorGroupRepository.display !== 'function') {
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
        : <BaseForm ComponentRepository={IndicatorGroupRepository} FormComponent={EnhancedIndicatorGroupForm}
          afterSaveRoute="/indicator-group/" title="Edit Indicator Group" initialFieldValues={data.indicatorGroupById} {...props}/>
    );
  }}
</Query>;
