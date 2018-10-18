import React from 'react';
import { shallow, mount } from 'enzyme';

import ListTableCell from './../../Components/ListTable/ListTableCell';

describe('ListTable unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(<ListTableCell contents="mock contents"/>);
  });

  it('renders', () => {
    expect(wrapper).toHaveLength(1);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('ListTable functional test', () => {
  it('renders correct contents', () => {
    const wrapper = mount(<table><tbody><tr><ListTableCell contents="mock contents"/></tr></tbody></table>);
    expect(wrapper.text()).toEqual('mock contents');
  });
});
