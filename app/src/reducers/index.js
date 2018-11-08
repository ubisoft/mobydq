import { combineReducers } from 'redux';
import { sidebarIsOpen } from './sidebar';
import { indicatorPage, indicatorRowsPerPage, indicatorRowTotal, indicatorSortColumn  } from './indicatorList';
import { indicatorGroupPage, indicatorGroupRowsPerPage, indicatorGroupRowTotal, indicatorGroupSortColumn  } from './indicatorGroupList';
import { dataSourcePage, dataSourceRowsPerPage, dataSourceRowTotal, dataSourceSortColumn } from './dataSourceList';

export default combineReducers({
  sidebarIsOpen,
  indicatorPage,
  indicatorRowsPerPage,
  indicatorRowTotal,
  indicatorSortColumn,
  indicatorGroupPage,
  indicatorGroupRowsPerPage,
  indicatorGroupRowTotal,
  indicatorGroupSortColumn,
  dataSourcePage,
  dataSourceRowsPerPage,
  dataSourceRowTotal,
  dataSourceSortColumn
});
