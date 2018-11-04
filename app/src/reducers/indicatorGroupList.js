export function indicatorGroupPage(state = 0, action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_PAGE':
      return action.page;
    default:
      return state;
  }
}

export function indicatorGroupRowsPerPage(state = 10, action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_ROWS_PER_PAGE':
      return action.rowsPerPage;
    default:
      return state;
  }
}

export function indicatorGroupRowTotal(state = 0, action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_ROW_TOTAL':
      return action.rowTotal;
    default:
      return state;
  }
}

export function indicatorGroupCurrentBatchId(state = -1, action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_CURRENT_BATCH_ID':
      return action.currentBatchId;
    default:
      return state;
  }
}

export function indicatorGroupMessage(state = '', action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_MESSAGE':
      return action.message;
    default:
      return state;
  }
}

export function indicatorGroupOpen(state = false, action) {
  switch (action.type) {
    case 'INDICATOR_GROUP_LIST_OPEN':
      return action.open;
    default:
      return state;
  }
}
