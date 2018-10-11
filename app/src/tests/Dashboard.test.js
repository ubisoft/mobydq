import React from 'react'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import Dashboard from './../Components/Dashboard/Dashboard';

it('renders empty dashboard crashing', () => {
  const wrapper = shallow(
    <Dashboard />
  );

  expect(wrapper).toMatchSnapshot();
});
