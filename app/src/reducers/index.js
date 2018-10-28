import { combineReducers } from 'redux';
import { sidebarIsOpen } from './sidebar';
import { indicatorPage, indicatorRowsPerPage, indicatorRowTotal } from './indicatorList';
import { indicatorGroupPage, indicatorGroupRowsPerPage, indicatorGroupRowTotal, indicatorGroupCurrentBatchId, indicatorGroupOpen, indicatorGroupMessage } from './indicatorGroupList';
import { dataSourcePage, dataSourceRowsPerPage, dataSourceRowTotal } from './dataSourceList';

export default combineReducers({
  sidebarIsOpen,
  indicatorPage,
  indicatorRowsPerPage,
  indicatorRowTotal,
  indicatorGroupPage,
  indicatorGroupRowsPerPage,
  indicatorGroupRowTotal,
  dataSourcePage,
  dataSourceRowsPerPage,
  dataSourceRowTotal,
  indicatorGroupCurrentBatchId,
  indicatorGroupOpen,
  indicatorGroupMessage
});
