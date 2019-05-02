export function userPage(state = 0, action) {
  switch (action.type) {
    case 'USER_LIST_PAGE':
      return action.page;
    default:
      return state;
  }
}

export function userRowsPerPage(state = 10, action) {
  switch (action.type) {
    case 'USER_LIST_ROWS_PER_PAGE':
      return action.rowsPerPage;
    default:
      return state;
  }
}

export function userRowTotal(state = 0, action) {
  switch (action.type) {
    case 'USER_LIST_ROW_TOTAL':
      return action.rowTotal;
    default:
      return state;
  }
}

export function userSortColumn(state = null, action) {
  switch (action.type) {
    case 'USER_LIST_SORT_COLUMN':
      return action.sortColumn;
    default:
      return state;
  }
}
