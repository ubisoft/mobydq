import React from 'react'
import { shallow, mount } from 'enzyme';

import {ListTableBody} from './../../Components/ListTable/ListTableBody'

describe('ListTableBody unit test', () => {
  let wrapper;
  let buttons = [{name: 'button name', function: jest.fn}];
  let content = [{id: 1, name: 'mock name', trueField: true, falseField: false},
                {id: 2, name: 'mock name 2', trueField: true, falseField: false}];
  let contentColumnList = ['id', 'name', 'trueField', 'falseField'];

  beforeEach(() => {
    wrapper = shallow(<ListTableBody buttons={buttons} content={content} contentColumnList={contentColumnList}/>)
  });

  it('renders', () => {
    expect(wrapper).toHaveLength(1);
    expect(wrapper.children()).toHaveLength(2);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('ListTableBody functional test', () => {
  it ('renders table body correctly, including boolean fields (True/False icons', () => {
    let buttons = [{name: 'button name', function: jest.fn}];
    let content = [{id: 1, name: 'mock name', trueField: true, falseField: false},
                {id: 2, name: 'mock name 2', trueField: false, falseField: false}];
    let contentColumnList = ['id', 'name', 'trueField', 'falseField'];
    let wrapper = mount(<table><ListTableBody content={content} contentColumnList={contentColumnList} buttons={buttons}/></table>);
    expect(wrapper.find('ListTableRowButtons').exists()).toBe(true);
    expect(wrapper.find('ListTableRowButtons')).toHaveLength(2);
    expect(wrapper.find('ListTableRowButtons').at(0).text()).toEqual('button name');
    expect(wrapper.find('ListTableRowButtons').at(1).text()).toEqual('button name');
    expect(wrapper.find('tr')).toHaveLength(2);
    expect(wrapper.find('td')).toHaveLength(10);
    expect(wrapper.find('td').at(0).text()).toEqual('1');
    expect(wrapper.find('td').at(1).text()).toEqual('mock name');
    expect(wrapper.find('td').at(5).text()).toEqual('2');
    expect(wrapper.find('td').at(6).text()).toEqual('mock name 2');
    expect(wrapper.find('DoneIcon')).toHaveLength(1);
    expect(wrapper.find('ClearIcon')).toHaveLength(3);
  });
  it ('renders empty table body correctly', () => {
    let buttons = [];
    let content = [];
    let contentColumnList = [];
    let wrapper = mount(<table><ListTableBody content={content} contentColumnList={contentColumnList} buttons={buttons}/></table>);
    expect(wrapper.text()).toEqual('');
  });
});