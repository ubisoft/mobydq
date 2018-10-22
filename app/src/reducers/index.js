import { combineReducers } from 'redux';
import { sidebarIsOpen } from './sidebar';
import { page, rowsPerPage, rowTotal } from './listTable'

export default combineReducers({
  sidebarIsOpen,
  page,
  rowsPerPage,
  rowTotal
});
