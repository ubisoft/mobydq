import React from 'react'
import { shallowWrap, mountWrap } from './../../setupTests'

import { MemoryRouter } from 'react-router-dom';
import { shape } from 'prop-types';

import {ListTableRowButtons} from './../../Components/ListTable/ListTableRowButtons'

describe('ListTableRowButtons unit test', () => {
  let wrapper;
  let buttons = [{'name': 'button name', 'function': 'edit', 'parameter': '/test-route'}];

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
    let buttons = [{'name': 'button name', 'function': 'edit', 'parameter': '/test-route'}, {'name': 'button name', 'function': 'delete', 'parameter': '/test-route'}];
    let wrapper = mountWrap(<table><tbody><tr><MemoryRouter><ListTableRowButtons buttons={buttons} value="1"/></MemoryRouter></tr></tbody></table>);
    expect(wrapper.find('EditIcon').exists()).toBe(true);
    expect(wrapper.find('DeleteIcon').exists()).toBe(true);
  });
  it ('renders correctly with no buttons', () => {
    let buttons = [];
    let wrapper = mountWrap(<table><tbody><tr><MemoryRouter><ListTableRowButtons buttons={buttons} value="1"/></MemoryRouter></tr></tbody></table>);
    expect(wrapper.text()).toEqual('');
  });
});