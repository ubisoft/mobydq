import React from 'react';
import { shallow, mount } from 'enzyme';

import { ListTableRowContent } from './../../Components/ListTable/ListTableRowContent';

describe('ListTableRowContent unit test', () => {
  let wrapper;
  const rowData = { 'id': 1, 'name': 'mock name' };
  const rowColumns = ['id', 'name'];
  beforeEach(() => {
    wrapper = shallow(<ListTableRowContent rowData={rowData} rowColumns={rowColumns} value="1"/>);
  });

  it('renders', () => {
    expect(wrapper).toHaveLength(2);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('ListTableRowContent functional test', () => {
  it('renders content row correctly, including boolean buttons', () => {
    const rowData = { 'id': 1, 'name': 'mock name', 'trueField': true, 'falseField': false };
    const rowColumns = ['id', 'name', 'trueField', 'falseField'];
    const wrapper = mount(<table><tbody><tr><ListTableRowContent rowData={rowData} rowColumns={rowColumns} /></tr></tbody></table>);
    expect(wrapper.find('tr')).toHaveLength(1);
    expect(wrapper.find('td')).toHaveLength(4);
    expect(wrapper.find('td').at(0)
      .text()).toEqual('1');
    expect(wrapper.find('td').at(1)
      .text()).toEqual('mock name');
    expect(wrapper.find('DoneIcon').exists()).toBe(true);
    expect(wrapper.find('ClearIcon').exists()).toEqual(true);
  });
  it('renders empty row correctly with no data', () => {
    const rowData = {};
    const rowColumns = [];
    const wrapper = mount(<table><tbody><tr><ListTableRowContent rowData={rowData} rowColumns={rowColumns} /></tr></tbody></table>);
    expect(wrapper.find('tr')).toHaveLength(1);
    expect(wrapper.find('td')).toHaveLength(0);
    expect(wrapper.text()).toEqual('');
  });
  it('renders empty row correctly with no data and provided headers    ', () => {
    const rowData = {};
    const rowColumns = ['id', 'name', 'trueField', 'falseField'];
    const wrapper = mount(<table><tbody><tr><ListTableRowContent rowData={rowData} rowColumns={rowColumns} /></tr></tbody></table>);
    expect(wrapper.find('tr')).toHaveLength(1);
    expect(wrapper.find('td')).toHaveLength(4);
    expect(wrapper.text()).toEqual('');
  });
});
