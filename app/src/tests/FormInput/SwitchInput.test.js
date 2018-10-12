import React from 'react'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow, mount } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import SwitchInput from '../../Components/FormInput/SwitchInput';

describe('SwitchInput unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <SwitchInput
        id="Id"
        label="Label"
        touched={jest.fn()}
        error={false}
        value="value"
        onChange={jest.fn()}
        onBlur={jest.fn()}
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