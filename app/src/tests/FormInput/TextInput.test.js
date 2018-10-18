import React from 'react';
import { shallow, mount } from 'enzyme';

import TextInput from '../../Components/FormInput/TextInput';

describe('TextInput unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <TextInput
        id="Id"
        label="Label"
        helperText="Helper Text"
        placeholder="Enter indicator name"
        touched="true"
        error=""
        value="value"
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

describe('TextInput functional test', () => {
  const wrapper = mount(
    <TextInput
      id="Id"
      label="Label"
      helperText="Helper Text"
      placeholder="Enter indicator name"
      touched="true"
      error=""
      value="mock text"
      onChange={jest.fn()}
      onBlur={jest.fn()}
    />
  );
  it('renders correct contents', () => {
    expect(wrapper.prop('value')).toEqual('mock text');
  });
  it('renders correct contents using setProps', () => {
    wrapper.setProps({ 'value': 'new mock content' });
    expect(wrapper.prop('value')).toEqual('new mock content');
  });
  it('renders correct numeric contents', () => {
    wrapper.setProps({ 'numeric': true, 'value': '123321' });
    expect(wrapper.prop('value')).toEqual('123321');
  });
});
