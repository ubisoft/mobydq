import React from 'react'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow, mount } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import ListTableCell from './../../Components/ListTable/ListTableCell'

describe('ListTable unit test', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(<ListTableCell contents='mock contents'/>)
  });

  it('renders', () => {
    expect(wrapper.length).toEqual(1);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('ListTable functional test', () => {
  it ('renders correct contents', () => {
    let wrapper = mount(<table><tbody><tr><ListTableCell contents='mock contents'/></tr></tbody></table>);
    expect(wrapper.text()).toEqual('mock contents')
  });
});