import React from 'react'
import { StaticRouter } from 'react-router'
import { shallow } from 'enzyme';

import Indicator from './../../Components/Indicator/Indicator'

test('Link matches snapshot', () => {
  const context = {};
  const wrapper = shallow(
    <StaticRouter location="/indicator" context={context}>
      <Indicator/>
    </StaticRouter>
  );

  expect(wrapper).toMatchSnapshot();
});