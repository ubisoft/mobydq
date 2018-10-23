import { combineReducers } from 'redux';
import { sidebarIsOpen } from './sidebar';
import { indicatorGroupPage, indicatorGroupRowsPerPage, indicatorGroupRowTotal } from './indicatorGroupList'

export default combineReducers({
  sidebarIsOpen,
  indicatorGroupPage,
  indicatorGroupRowsPerPage,
  indicatorGroupRowTotal
});
