export function setUserGroupPage(int) {
  return {
    'type': 'USER_GROUP_LIST_PAGE',
    'page': int
  };
}

export function setUserGroupRowsPerPage(int) {
  return {
    'type': 'USER_GROUP_LIST_ROWS_PER_PAGE',
    'rowsPerPage': int
  };
}

export function setUserGroupRowTotal(int) {
  return {
    'type': 'USER_GROUP_LIST_ROW_TOTAL',
    'rowTotal': int
  };
}

export function setUserGroupSortColumn(string) {
  return {
    'type': 'USER_GROUP_LIST_SORT_COLUMN',
    'sortColumn': string
  };
}
