import React from 'react'
import { MemoryRouter } from 'react-router';
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow, mount } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import RouterButton from '../../Components/FormInput/RouterButton';

describe('TextInput unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <RouterButton
        history=''
        targetLocation='/'
        label='test button'
        disabled={false}
      />
    );
  });

  it('renders', () => {
    expect(wrapper.length).toEqual(1);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});
// todo fix react router tests
//describe('TextInput functional test', () => {
//  let context = {};
//  let history = {};
//  let wrapper;
//  beforeEach(() => {
//    wrapper = mount(
//      <MemoryRouter initialEntries={[ '/random' ]}>
//        <RouterButton
//          history=''
//          targetLocation='back'
//          label='test button'
//          disabled={true}
//        />
//      </MemoryRouter>
//    );
//  });
//
//  it('renders', () => {
//    expect(wrapper.length).toEqual(1);
//  });
//
//  it('matches snapshot', () => {
//    expect(wrapper).toMatchSnapshot();
//  });
//});
