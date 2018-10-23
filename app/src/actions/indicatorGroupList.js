export function setIndicatorGroupPage(int) {
  return {
    'type': 'INDICATOR_GROUP_LIST_PAGE',
    'page': int
  };
}

export function setIndicatorGroupRowsPerPage(int) {
  return {
    'type': 'INDICATOR_GROUP_LIST_ROWS_PER_PAGE',
    'rowsPerPage': int
  };
}

export function setIndicatorGroupRowTotal(int) {
  return {
    'type': 'INDICATOR_GROUP_LIST_ROW_TOTAL',
    'rowTotal': int
  };
}