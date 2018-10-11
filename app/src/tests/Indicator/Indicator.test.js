import React from 'react'
import { StaticRouter } from 'react-router'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

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