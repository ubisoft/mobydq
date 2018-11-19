import React from 'react';
import { shallow } from 'enzyme';

import Dashboard from './../Components/Dashboard/Dashboard';

it('renders empty dashboard crashing', () => {
  const wrapper = shallow(
    <Dashboard />
  );

  expect(wrapper).toMatchSnapshot();
});
