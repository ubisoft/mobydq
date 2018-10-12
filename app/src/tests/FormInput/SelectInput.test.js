import React from 'react';
import { shallow, mount } from 'enzyme';

import SelectInput from '../../Components/FormInput/SelectInput';

describe('SelectInput unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <SelectInput
        id="Id"
        label="Label"
        items={[{id: 1, name: 'select value 1'}, {id: 2, name: 'select value 2'}]}
        helperText="Helper Text"
        placeholder="Select indicator type"
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

describe('SelectInput functional test', () => {
  let wrapper = mount(
      <SelectInput
        id="Id"
        label="Label"
        items={[{id: 1, name: 'select value 1'}, {id: 2, name: 'select value 2'}]}
        placeholder="Select indicator type"
        touched="true"
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
