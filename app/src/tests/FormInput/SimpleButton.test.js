import React from 'react';
import { shallow, mount } from 'enzyme';

import SimpleButton from '../../Components/FormInput/SimpleButton';

describe('SimpleButton unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(
      <SimpleButton
        type="submit"
        disabled={false}
        label="Button"
        variant="contained"
        color="primary"
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
  const wrapper = mount(
    <SimpleButton
      type="submit"
      disabled={false}
      label="Button"
      variant="contained"
      color="primary"
      onClick={jest.fn()}
    />
  );
  it('renders correct primary button', () => {
    expect(wrapper.prop('type')).toEqual('submit');
    expect(wrapper.find('Button').prop('color')).toEqual('primary');
  });
});
