import Enzyme, { shallow, render, mount } from 'enzyme';
import EnzymeAdapter from 'enzyme-adapter-react-16';
import { BrowserRouter } from 'react-router-dom';

import { shape } from 'prop-types';

// Setup enzyme's react adapter
Enzyme.configure({ adapter: new EnzymeAdapter() });

// Make Enzyme functions available in all test files without importing
global.shallow = shallow;
global.render = render;
global.mount = mount;

// Instantiate router context
const router = {
  history: new BrowserRouter().history,
  route: {
    location: {},
    match: {},
  },
};

const createContext = () => ({
  context: { router },
  childContextTypes: { router: shape({}) },
});
// export router context mounts
export function mountWrap(node) {
  return mount(node, createContext());
}

export function shallowWrap(node) {
  return shallow(node, createContext());
}