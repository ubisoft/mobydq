import React from 'react'
import { shallow } from 'enzyme';

import RouterButton from '../../Components/FormInput/RouterButton';

describe('RouterButton unit test', () => {
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
    expect(wrapper).toHaveLength(1);
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
