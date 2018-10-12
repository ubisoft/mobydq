import React from 'react'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow, mount } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import ListTableHeader from './../../Components/ListTable/ListTableHeader'

describe('ListTableHeader unit test', () => {
  let wrapper;
  let headerNames = ['id', 'name', 'longName', ''];

  beforeEach(() => {
    wrapper = shallow(<ListTableHeader headerNames={headerNames}/>)
  });

  it('renders', () => {
    expect(wrapper.length).toEqual(1);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('ListTableHeader functional test', () => {
  it ('renders properly capitalizes the names and renders the action column', () => {
    let headerNames = ['id', 'name', 'longName', ''];
    let wrapper = mount(<table><ListTableHeader headerNames={headerNames}/></table>);
    expect(wrapper.find('tr').length).toEqual(1);
    expect(wrapper.find('th').length).toEqual(5);
    expect(wrapper.find('th').at(0).text()).toEqual('Id');
    expect(wrapper.find('th').at(1).text()).toEqual('Name');
    expect(wrapper.find('th').at(2).text()).toEqual('Long Name');
    expect(wrapper.find('th').at(3).text()).toEqual('');
    expect(wrapper.find('th').at(4).text()).toEqual('Actions');
  });
  it ('renders correctly with no headers', () => {
    let headerNames = [];
    let wrapper = mount(<table><ListTableHeader headerNames={headerNames}/></table>);
    expect(wrapper.find('tr').length).toEqual(1);
    expect(wrapper.find('th').length).toEqual(1);
    expect(wrapper.find('th').at(0).text()).toEqual('Actions');

  });
});