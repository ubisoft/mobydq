import React from 'react'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow, mount } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import ListTable from '../../Components/ListTable/ListTable';

describe('List Table unit test', () => {
  let wrapper;
  let buttons = [{name: 'button name', function: jest.fn}];
  let data = [{id: 1, name: 'mock name', trueField: true, falseField: false, __typename: 'Mock Type'},
              {id: 2, name: 'mock name 2', trueField: false, falseField: false, __typename: 'Mock Type'}];
  beforeEach(() => {
    wrapper = shallow(<ListTable buttons={buttons} data={data}/>)
  });

  it('renders', () => {
    expect(wrapper.length).toEqual(1);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});


describe('ListTable functional test', () => {
  it ('renders table correctly, including boolean fields (True/False icons', () => {
    let buttons = [{name: 'button name', function: jest.fn}];
    let data = [{id: 1, name: 'mock name', trueField: true, falseField: false, __typename: 'Mock Type'},
                {id: 2, name: 'mock name 2', trueField: false, falseField: false, __typename: 'Mock Type'}];
    let wrapper = mount(<ListTable buttons={buttons} data={data}/>);
    expect(wrapper.find('ListTableRowButtons').exists()).toBe(true);
    expect(wrapper.find('ListTableRowButtons').length).toEqual(2);
    expect(wrapper.find('ListTableRowButtons').at(0).text()).toEqual('button name');
    expect(wrapper.find('ListTableRowButtons').at(1).text()).toEqual('button name');
    expect(wrapper.find('tr').length).toEqual(3);
    expect(wrapper.find('td').length).toEqual(10);
    expect(wrapper.find('th').length).toEqual(5);
    expect(wrapper.find('th').at(0).text()).toEqual('Id');
    expect(wrapper.find('th').at(1).text()).toEqual('Name');
    expect(wrapper.find('th').at(2).text()).toEqual('True Field');
    expect(wrapper.find('th').at(3).text()).toEqual('False Field');
    expect(wrapper.find('th').at(4).text()).toEqual('Actions');
    expect(wrapper.find('th').at(0).text()).toEqual('Id');
    expect(wrapper.find('th').at(1).text()).toEqual('Name');
    expect(wrapper.find('td').at(0).text()).toEqual('1');
    expect(wrapper.find('td').at(1).text()).toEqual('mock name');
    expect(wrapper.find('td').at(5).text()).toEqual('2');
    expect(wrapper.find('td').at(6).text()).toEqual('mock name 2');
    expect(wrapper.find('DoneIcon').length).toEqual(1);
    expect(wrapper.find('ClearIcon').length).toEqual(3);
  });
  it ('renders empty table body correctly', () => {
    let buttons = [];
    let data = [];
    let wrapper = mount(<ListTable buttons={buttons} data={data}/>);
    expect(wrapper.text()).toEqual(null);
  });
});