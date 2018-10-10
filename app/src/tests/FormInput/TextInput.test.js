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


