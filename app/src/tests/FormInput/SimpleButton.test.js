import React from 'react'
import { shallow, mount } from 'enzyme';

import SimpleButton from '../../Components/FormInput/SimpleButton';

describe('SimpleButton unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <SimpleButton
        type='submit'
        disabled={false}
        label='Button'
        variant='contained'
        onClick={jest.fn()}
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

describe('SimpleButton functional test', () => {
  let wrapper = mount(
      <SimpleButton
        type='submit'
        disabled={false}
        label='Button'
        variant='contained'
        onClick={jest.fn()}
      />
    );
  it ('renders correct submit button', () => {
    expect(wrapper.prop('type')).toEqual('submit')
    expect(wrapper.find('Button').prop('color')).toEqual('primary')
  });
  it ('renders correct reset button', () => {
    wrapper.setProps({type: 'reset'})
    expect(wrapper.find('Button').prop('color')).toEqual('secondary')
  });
  it ('renders correct cancel button', () => {
    wrapper.setProps({type: 'cancel'})
    expect(wrapper.find('Button').prop('color')).toEqual('default')
  });
  it ('renders correct create button', () => {
    wrapper.setProps({type: 'create'})
    expect(wrapper.find('Button').prop('color')).toEqual('primary')
  });
  it ('renders correct default button', () => {
    wrapper.setProps({type: 'foo'})
    expect(wrapper.find('Button').prop('color')).toEqual('default')
  });
});
