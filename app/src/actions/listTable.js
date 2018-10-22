export function setPage(int) {
  return {
    'type': 'LIST_TABLE_PAGE',
    'page': int
  };
}

export function setRowsPerPage(int) {
  return {
    'type': 'LIST_TABLE_ROWS_PER_PAGE',
    'rowsPerPage': int
  };
}

export function setRowTotal(int) {
  return {
    'type': 'LIST_TABLE_ROW_TOTAL',
    'rowTotal': int
  };
}