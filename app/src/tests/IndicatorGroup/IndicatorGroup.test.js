import React from 'react';
import { shallowWrap } from './../../setupTests';

import IndicatorGroup from './../../Components/IndicatorGroup/IndicatorGroup';

describe('IndicatorGroup component unit test', () => {
  const match = {
    'url': '/indicator-group'
  };
  const wrapper = shallowWrap(<IndicatorGroup match={match}/>);
  it('matches snapshot', () => {
    expect(wrapper.dive()).toMatchSnapshot();
  });
  it('contains exactly 3 routes', () => {
    expect(wrapper.dive().find('Route')).toHaveLength(3);
  });
});
