import React from 'react';
import { shallowWrap } from './../../setupTests';

import { MemoryRouter } from 'react-router-dom';

import { UnauthorizedError } from '../../Components/Error/UnauthorizedError';
import LinkButton from './../../Components/FormInput/LinkButton';

describe('UnauthorizedError component unit test', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowWrap(
      <UnauthorizedError/>
    );
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('UnauthorizedError component functional test', () => {
  it('renders the UnauthorizedError component', () => {
    const wrapper = mount(<div><MemoryRouter><UnauthorizedError/></MemoryRouter></div>);
    const loginButton = <LinkButton label="Re-login" color="secondary" variant="contained" to={'/login'}/>;
    expect(wrapper.contains(loginButton)).toEqual(true);
  });
});