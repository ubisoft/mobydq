import React from 'react';
import { shallowWrap } from './../../setupTests';

import Indicator from './../../Components/Indicator/Indicator';

describe('indicator component unit test', () => {
  const match = {
    'url': '/indicator'
  };
  const wrapper = shallowWrap(<Indicator match={match}/>);
  it('matches snapshot', () => {
    expect(wrapper.dive()).toMatchSnapshot();
  });
});
