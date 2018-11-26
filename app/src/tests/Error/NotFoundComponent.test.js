import React from 'react';
import { shallowWrap, mountWrap } from './../../setupTests';

import NotFoundComponent from '../../Components/Error/NotFoundComponent';

describe('NotFoundError component unit test', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowWrap(
      <NotFoundComponent/>
    );
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('error component functional test', () => {
  it('renders the NotFoundError component', () => {
    const wrapper = mountWrap(<div><NotFoundComponent/></div>);
    const errorMessage = <h1>404 Not Found</h1>;
    expect(wrapper.contains(errorMessage)).toEqual(true);
  });
});
