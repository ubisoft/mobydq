import React from 'react';
import { shallowWrap } from './../../setupTests';

import IndicatorGroupForm from './../../Components/IndicatorGroup/IndicatorGroupForm';

describe('IndicatorGroupForm component unit test', () => {
  const data = {};

  const wrapper = shallowWrap(<IndicatorGroupForm data={data} initialFieldValues={null} handleBlur={jest.fn()} handleChange={jest.fn()} handleSubmit={jest.fn()} isSubmitting={false}/>);
  it('matches snapshot', () => {
    expect(wrapper.dive()).toMatchSnapshot();
  });
});
