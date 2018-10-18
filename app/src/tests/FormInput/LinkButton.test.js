import React from 'react';
import { shallowWrap } from './../../setupTests';

import LinkButton from '../../Components/FormInput/LinkButton';

describe('LinkButton unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallowWrap(
      <LinkButton
        type="submit"
        disabled={false}
        label="Button"
        variant="contained"
        color="primary"
        to="/"
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
