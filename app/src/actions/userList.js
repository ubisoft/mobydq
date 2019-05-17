export function setUserPage(int) {
  return {
    'type': 'USER_LIST_PAGE',
    'page': int
  };
}

export function setUserRowsPerPage(int) {
  return {
    'type': 'USER_LIST_ROWS_PER_PAGE',
    'rowsPerPage': int
  };
}

export function setUserRowTotal(int) {
  return {
    'type': 'USER_LIST_ROW_TOTAL',
    'rowTotal': int
  };
}

export function setUserSortColumn(string) {
  return {
    'type': 'USER_LIST_SORT_COLUMN',
    'sortColumn': string
  };
}
