import React from 'react'
import renderer from 'react-test-renderer';

import TextInput from '../../Components/FormInput/TextInput';


it('renders TextInput without crashing with good props', () => {
  const data = "not an array";


  const component = renderer.create(
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

  let tree = component.toJSON();

  expect(tree).toMatchSnapshot();
});

it('renders TextInput without crashing with good props and error set', () => {
  const data = "not an array";


  const component = renderer.create(
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

  let tree = component.toJSON();

  expect(tree).toMatchSnapshot();
});


it('renders TextInput without crashing if id is not set or value is empty', () => {
  const data = "not an array";


  const component = renderer.create(
    <TextInput
          id=""
          label="Label"
          helperText="Helper Text"
          placeholder="Enter indicator name"
          touched={null}
          error="an error text"
          value=""
          onChange={null}
          onBlur={null}
          style={{ float: 'left' }}
        />
  );

  let tree = component.toJSON();

  expect(tree).toMatchSnapshot();
});

it('renders a numeric TextInput without crashing', () => {
  const data = "not an array";


  const component = renderer.create(
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

  let tree = component.toJSON();

  expect(tree).toMatchSnapshot();
});

