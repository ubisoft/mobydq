import React from 'react';
import { shallow, mount } from 'enzyme';

import ListTableHeader from './../../Components/ListTable/ListTableHeader';

describe('ListTableHeader unit test', () => {
  let wrapper;
  const headerNames = ['id', 'name', 'longName', ''];
  const params = {
    'sortColumn': null
  };

  beforeEach(() => {
    wrapper = shallow(<ListTableHeader headerNames={headerNames} params={params}/>);
  });

  it('renders', () => {
    expect(wrapper).toHaveLength(1);
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('ListTableHeader functional test', () => {
  const params = {
    'sortColumn': null
  };
  it('renders properly capitalizes the names and renders the action column', () => {
    const headerNames = ['id', 'name', 'longName', ''];
    const wrapper = mount(<table><ListTableHeader headerNames={headerNames} params={params}/></table>);
    expect(wrapper.find('tr')).toHaveLength(1);
    expect(wrapper.find('th')).toHaveLength(5);
    expect(wrapper.find('th').at(0)
      .text()).toEqual('Id');
    expect(wrapper.find('th').at(1)
      .text()).toEqual('Name');
    expect(wrapper.find('th').at(2)
      .text()).toEqual('Long Name');
    expect(wrapper.find('th').at(3)
      .text()).toEqual('');
    expect(wrapper.find('th').at(4)
      .text()).toEqual('Actions');
  });
  it('renders correctly with no headers', () => {
    const headerNames = [];
    const wrapper = mount(<table><ListTableHeader headerNames={headerNames} params={params}/></table>);
    expect(wrapper.find('tr')).toHaveLength(1);
    expect(wrapper.find('th')).toHaveLength(1);
    expect(wrapper.find('th').at(0)
      .text()).toEqual('Actions');
  });
});
