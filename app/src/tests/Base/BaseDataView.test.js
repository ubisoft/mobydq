import React from 'react';
import { shallowWrap } from './../../setupTests';


import BaseDataView from './../../Components/Base/BaseDataView';

describe('BaseDataView component unit test', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowWrap(
      <BaseDataView/>
    );
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});
