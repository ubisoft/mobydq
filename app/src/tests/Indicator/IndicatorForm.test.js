import React from 'react';
import { shallowWrap } from './../../setupTests';

import IndicatorForm from './../../Components/Indicator/IndicatorForm';

describe('IndicatorForm component unit test', () => {
  const data = {
    'allIndicatorGroups': {
      'nodes': [
        {
          'id': 1,
          'value': 'mock indicator group'
        }
      ]
    },
    'allIndicatorTypes': {
      'nodes': [
        {
          'id': 1,
          'value': 'mock indicator type'
        }
      ]
    }
  };

  const wrapper = shallowWrap(<IndicatorForm data={data} initialFieldValues={null} handleBlur={jest.fn()} handleChange={jest.fn()} handleSubmit={jest.fn()} isSubmitting={false}/>);
  it('matches snapshot', () => {
    expect(wrapper.dive()).toMatchSnapshot();
  });
});
