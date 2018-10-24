export function dataSourcePage(state = 0, action) {
  switch (action.type) {
  case 'DATA_SOURCE_LIST_PAGE':
    return action.page;
  default:
    return state;
  }
}

export function dataSourceRowsPerPage(state = 10, action) {
  switch (action.type) {
  case 'DATA_SOURCE_LIST_ROWS_PER_PAGE':
    return action.rowsPerPage;
  default:
    return state;
  }
}

export function dataSourceRowTotal(state = 0, action) {
  switch (action.type) {
  case 'DATA_SOURCE_LIST_ROW_TOTAL':
    return action.rowTotal;
  default:
    return state;
  }
}
