import React from 'react'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow, mount } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import SelectInput from '../../Components/FormInput/SelectInput';

describe('TextInput unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <SelectInput
        id="Id"
        label="Label"
        items={[{id: 1, name: 'select value 1'}, {id: 2, name: 'select value 2'}]}
        helperText="Helper Text"
        placeholder="Enter indicator name"
        touched={jest.fn()}
        error=""
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

describe('TextInput functional test', () => {
  let wrapper = mount(
      <SelectInput
        id="Id"
        label="Label"
        items={[{id: 1, name: 'select value 1'}, {id: 2, name: 'select value 2'}]}
        helperText="Helper Text"
        placeholder="Enter indicator name"
        touched={jest.fn()}
        error=""
        value={1}
        onChange={jest.fn()}
        onBlur={jest.fn()}
      />
    );
  it ('renders correct contents', () => {
    expect(wrapper.prop('value')).toEqual(1)
  });
});
