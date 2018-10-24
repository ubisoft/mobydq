export function setDataSourcePage(int) {
  return {
    'type': 'DATA_SOURCE_LIST_PAGE',
    'page': int
  };
}

export function setDataSourceRowsPerPage(int) {
  return {
    'type': 'DATA_SOURCE_LIST_ROWS_PER_PAGE',
    'rowsPerPage': int
  };
}

export function setDataSourceRowTotal(int) {
  return {
    'type': 'DATA_SOURCE_LIST_ROW_TOTAL',
    'rowTotal': int
  };
}
