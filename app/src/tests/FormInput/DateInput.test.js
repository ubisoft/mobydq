import React from 'react';
import { shallow, mount } from 'enzyme';

import DateInput from '../../Components/FormInput/DateInput';

describe('DateInput unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <DateInput
        id="Id"
        label="Label"
        helperText="Helper Text"
        placeholder="Enter date"
        touched="true"
        error=""
        value="2018-10-11"
        onChange={jest.fn()}
        onBlur={jest.fn()}
      />
    );
  });

  it('renders', () => {
    expect(wrapper).toHaveLength(1);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('DateInput functional test', () => {
  const wrapper = mount(
    <DateInput
      id="Id"
      label="Label"
      helperText="Helper Text"
      placeholder="Enter date"
      touched="true"
      error=""
      value="2018-10-11"
      onChange={jest.fn()}
      onBlur={jest.fn()}
    />
  );
  it('renders', () => {
    expect(wrapper).toHaveLength(1);
  });
});
