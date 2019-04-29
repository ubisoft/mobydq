export function userGroupPage(state = 0, action) {
  switch (action.type) {
    case 'USER_GROUP_LIST_PAGE':
      return action.page;
    default:
      return state;
  }
}

export function userGroupRowsPerPage(state = 10, action) {
  switch (action.type) {
    case 'USER_GROUP_LIST_ROWS_PER_PAGE':
      return action.rowsPerPage;
    default:
      return state;
  }
}

export function userGroupRowTotal(state = 0, action) {
  switch (action.type) {
    case 'USER_GROUP_LIST_ROW_TOTAL':
      return action.rowTotal;
    default:
      return state;
  }
}

export function userGroupSortColumn(state = null, action) {
  switch (action.type) {
    case 'USER_GROUP_LIST_SORT_COLUMN':
      return action.sortColumn;
    default:
      return state;
  }
}
