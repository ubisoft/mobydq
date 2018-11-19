import React from 'react';
import { shallow, mount } from 'enzyme';

import CheckboxInput from '../../Components/FormInput/CheckboxInput';

describe('CheckboxInput unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <CheckboxInput
        id="Id"
        label="Label"
        helperText="Helper Text"
        placeholder="Are you an indicator?"
        touched="true"
        error=""
        value="true"
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

describe('CheckboxInput functional test', () => {
  const wrapper = mount(
    <CheckboxInput
      id="Id"
      label="Label"
      placeholder="Are you an indicator?"
      touched="true"
      error=""
      value="true"
      onChange={jest.fn()}
      onBlur={jest.fn()}
    />
  );
  it('renders', () => {
    expect(wrapper).toHaveLength(1);
  });
});
