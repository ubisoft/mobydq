export function indicatorPage(state = 0, action) {
  switch (action.type) {
  case 'INDICATOR_LIST_PAGE':
    return action.page;
  default:
    return state;
  }
}

export function indicatorRowsPerPage(state = 10, action) {
  switch (action.type) {
  case 'INDICATOR_LIST_ROWS_PER_PAGE':
    return action.rowsPerPage;
  default:
    return state;
  }
}

export function indicatorRowTotal(state = 0, action) {
  switch (action.type) {
  case 'INDICATOR_LIST_ROW_TOTAL':
    return action.rowTotal;
  default:
    return state;
  }
}

export function indicatorSortColumn(state = null, action) {
  switch (action.type) {
  case 'INDICATOR_LIST_SORT_COLUMN':
    return action.sortColumn;
  default:
    return state;
  }
}
