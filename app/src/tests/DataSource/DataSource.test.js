import React from 'react';
import { shallowWrap } from './../../setupTests';

import DataSource from './../../Components/DataSource/DataSource';

describe('DataSource component unit test', () => {
  const match = {
    'url': '/data-source'
  };
  const wrapper = shallowWrap(<DataSource match={match}/>);
  it('matches snapshot', () => {
    expect(wrapper.dive()).toMatchSnapshot();
  });
  it('contains exactly 3 routes', () => {
    expect(wrapper.dive().find('Route')).toHaveLength(3);
  });
});
