import React from 'react'
import { shallowWrap, mountWrap } from './../../setupTests'
//import DataSourceRepository from '../../repository/DataSourceRepository'

import { MemoryRouter } from 'react-router-dom';

import {ListTableRowButtons} from './../../Components/ListTable/ListTableRowButtons'

describe('ListTableRowButtons unit test', () => {
  let wrapper;
  let buttons = [{'function': 'edit', 'parameter': '/test-route'}];

  beforeEach(() => {
    wrapper = shallowWrap(<ListTableRowButtons buttons={buttons} value="1"/>)
  });

  it('renders', () => {
    expect(wrapper).toHaveLength(1);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('ListTableRowButtons functional test', () => {
  it ('renders buttons correctly', () => {
//    let buttons = [{'name': 'edit', 'parameter': '/test-route'}, {'name': 'delete', 'parameter': DataSourceRepository}];
//todo rewrite test when apollo testing is implemented
    let buttons = [{'function': 'edit', 'parameter': '/test-route'}];
    let wrapper = mountWrap(<table><tbody><tr><MemoryRouter><ListTableRowButtons buttons={buttons} value="1"/></MemoryRouter></tr></tbody></table>);
    expect(wrapper.find('EditIcon').exists()).toBe(true);

//todo rewrite test when apollo testing is implemented
//    expect(wrapper.find('DeleteIcon').exists()).toBe(true);
  });
  it ('renders correctly with no buttons', () => {
    let buttons = [];
    let wrapper = mountWrap(<table><tbody><tr><MemoryRouter><ListTableRowButtons buttons={buttons} value="1"/></MemoryRouter></tr></tbody></table>);
    expect(wrapper.text()).toEqual('');
  });
});