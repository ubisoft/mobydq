import React from 'react'
import renderer from 'react-test-renderer';
import { StaticRouter } from 'react-router'

import Indicator from './../Indicator/IndicatorTest'

test('Link matches snapshot', () => {
  const component = renderer.create(
    <StaticRouter location="/indicator" context={context}>
      <Indicator/>
    </StaticRouter>
  );

  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});