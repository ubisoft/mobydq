import React from 'react'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import TextInput from '../../Components/FormInput/TextInput';

//configure({adapter: new Adapter()});

test('renders TextInput without crashing with good props', () => {
  const data = "not an array";


  const wrapper = shallow(
    <TextInput
          id="Id"
          label="Label"
          helperText="Helper Text"
          placeholder="Enter indicator name"
          touched={null}
          error=""
          value="value"
          onChange={null}
          onBlur={null}
          style={{ float: 'left' }}
        />
  );

  expect(wrapper).toMatchSnapshot();
});

test('renders TextInput without crashing with good props and error set', () => {
  const data = "not an array";


  const wrapper = shallow(
    <TextInput
          id="Id"
          label="Label"
          helperText="Helper Text"
          placeholder="Enter indicator name"
          touched={null}
          error="an error text"
          value="value"
          onChange={null}
          onBlur={null}
          style={{ float: 'left' }}
        />
  );

  expect(wrapper).toMatchSnapshot();
});


test('renders TextInput without crashing if id is not set or value is empty', () => {
  const data = "not an array";


  const wrapper = shallow(
    <TextInput
          id=""
          label="Label"
          helperText="Helper Text"
          placeholder="Enter indicator name"
          touched={null}
          error="an error text"
          value=""
          onChange={jest.fn()}
          onBlur={null}
          style={{ float: 'left' }}
        />
  );

  expect(wrapper).toMatchSnapshot();
});

test('renders a numeric TextInput without crashing', () => {
  const data = "not an array";


  const wrapper = shallow(
    <TextInput
          id="Id"
          label="Label"
          helperText="Helper Text"
          placeholder="Enter indicator name"
          touched={null}
          error="an error text"
          value="1323"
          onChange={null}
          onBlur={null}
          numeric
        />
  );

  expect(wrapper).toMatchSnapshot();
});
