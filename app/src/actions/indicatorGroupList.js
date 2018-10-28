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

export function setIndicatorGroupMessage(str) {
  return {
    'type': 'INDICATOR_GROUP_LIST_MESSAGE',
    'message': str
  };
}

export function setIndicatorGroupOpen(bool) {
  return {
    'type': 'INDICATOR_GROUP_LIST_OPEN',
    'open': bool
  };
}

export function setIndicatorGroupCurrentBatchId(int) {
  return {
    'type': 'INDICATOR_GROUP_LIST_CURRENT_BATCH_ID',
    'currentBatchId': int
  };
}
