import React from 'react';
import { shallowWrap, mountWrap } from './../../setupTests';
import configureStore from 'redux-mock-store';
import { MemoryRouter } from 'react-router-dom';


import BaseDataView from './../../Components/Base/BaseDataView';

describe('BaseDataView component unit test', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowWrap(
      <BaseDataView/>
    );
  });

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

describe('BaseDataView component functional test', () => {
  let wrapper;
  const initialState = { 'sidebarIsOpen': false };
  const mockStore = configureStore();
  const store = mockStore(initialState);
  it('renders the BaseDataView component with sidebar closed', () => {
    wrapper = mountWrap(<div><MemoryRouter><BaseDataView store={store}/></MemoryRouter></div>);
    expect(wrapper.find('AppBar').length === 1).toEqual(true);
    wrapper.find('IconButton').first().simulate('click');
  });

  it('renders the BaseDataView component with sidebar sidebarIsOpen', () => {
    store.open = true;
    wrapper = mountWrap(<div><MemoryRouter><BaseDataView store={store}/></MemoryRouter></div>);
    expect(wrapper.find('AppBar').length === 1).toEqual(true);
    wrapper.find('IconButton').first().simulate('click');
  });
});
