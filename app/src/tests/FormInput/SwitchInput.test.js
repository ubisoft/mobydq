import React from 'react'
import { shallow, mount } from 'enzyme';

import SwitchInput from '../../Components/FormInput/SwitchInput';

describe('SwitchInput unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <SwitchInput
        id="Id"
        label="Label"
        touched={true}
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

describe('SwitchInput functional test', () => {
  let wrapper = mount(
      <SwitchInput
        id="Id"
        label="Label"
        touched="true"
        error=""
        value="true"
        onChange={jest.fn()}
        onBlur={jest.fn()}
      />
    );

  it('renders correct contents', () => {
    expect(wrapper.prop('value')).toEqual('true');
  });
});
