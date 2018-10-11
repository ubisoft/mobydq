import React from 'react'
import * as Adapter from 'enzyme-adapter-react-16';
import { shallow, mount } from 'enzyme';
import { shallowToJson } from 'enzyme-to-json';

import {ListTableRowButtons} from './../../Components/ListTable/ListTableRowButtons'

describe('ListTableRowButtons unit test', () => {
  let wrapper;
  let buttons = [{name: 'button name', function: jest.fn}];
  beforeEach(() => {
    wrapper = shallow(<ListTableRowButtons buttons={buttons} value="1"/>)
  });

  it('renders', () => {
    expect(wrapper.length).toEqual(1);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('ListTableRowButtons functional test', () => {
  it ('renders buttons correctly', () => {
    let buttons = [{name: 'button name', function: jest.fn}];
    let wrapper = mount(<table><tbody><tr><ListTableRowButtons buttons={buttons} value="1"/></tr></tbody></table>);
    expect(wrapper.text()).toEqual('button name');
  });
  it ('renders correctly with no buttons', () => {
    let buttons = [];
    let wrapper = mount(<table><tbody><tr><ListTableRowButtons buttons={buttons} value="1"/></tr></tbody></table>);
    expect(wrapper.text()).toEqual('');
  });
});