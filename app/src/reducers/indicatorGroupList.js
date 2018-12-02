export function indicatorGroupPage(state = 0, action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_PAGE':
      return action.page;
    default:
      return state;
  }
}

export function indicatorGroupRowsPerPage(state = 10, action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_ROWS_PER_PAGE':
      return action.rowsPerPage;
    default:
      return state;
  }
}

export function indicatorGroupRowTotal(state = 0, action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_ROW_TOTAL':
      return action.rowTotal;
    default:
      return state;
  }
}

export function indicatorGroupSortColumn(state = null, action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_SORT_COLUMN':
      return action.sortColumn;
    default:
      return state;
  }
}
