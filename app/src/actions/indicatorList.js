export function setIndicatorPage(int) {
  return {
    'type': 'INDICATOR_LIST_PAGE',
    'page': int
  };
}

export function setIndicatorRowsPerPage(int) {
  return {
    'type': 'INDICATOR_LIST_ROWS_PER_PAGE',
    'rowsPerPage': int
  };
}

export function setIndicatorRowTotal(int) {
  return {
    'type': 'INDICATOR_LIST_ROW_TOTAL',
    'rowTotal': int
  };
}
