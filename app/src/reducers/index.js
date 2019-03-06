import { combineReducers } from 'redux';
import { sidebarIsOpen } from './sidebar';
import { indicatorPage, indicatorRowsPerPage, indicatorRowTotal, indicatorSortColumn } from './indicatorList';
import { indicatorGroupPage, indicatorGroupRowsPerPage, indicatorGroupRowTotal, indicatorGroupSortColumn } from './indicatorGroupList';
import { userGroupPage, userGroupRowsPerPage, userGroupRowTotal, userGroupSortColumn } from './userGroupList';
import { dataSourcePage, dataSourceRowsPerPage, dataSourceRowTotal, dataSourceSortColumn } from './dataSourceList';
import { messageBarIsOpen, messageBarMessage } from './messageBar';
import { userMenuAnchor } from './topbar';
import { alertDialog } from './app';

export default combineReducers({
  alertDialog,
  sidebarIsOpen,
  userMenuAnchor,
  indicatorPage,
  indicatorRowsPerPage,
  indicatorRowTotal,
  indicatorSortColumn,
  indicatorGroupPage,
  indicatorGroupRowsPerPage,
  indicatorGroupRowTotal,
  indicatorGroupSortColumn,
  messageBarIsOpen,
  messageBarMessage,
  dataSourcePage,
  dataSourceRowsPerPage,
  dataSourceRowTotal,
  dataSourceSortColumn,
  userGroupPage,
  userGroupRowsPerPage,
  userGroupRowTotal,
  userGroupSortColumn
});
