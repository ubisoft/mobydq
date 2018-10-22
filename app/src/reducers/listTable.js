export function page(state = 0, action) {
  switch (action.type) {
    case 'LIST_TABLE_PAGE':
      return action.page;
    default:
      return state;
  }
}

export function rowsPerPage(state = 10, action) {
  switch (action.type) {
    case 'LIST_TABLE_ROWS_PER_PAGE':
      return action.rowsPerPage;
    default:
      return state;
  }
}

export function rowTotal(state = 0, action) {
  switch (action.type) {
    case 'LIST_TABLE_ROW_TOTAL':
      return action.rowTotal;
    default:
      return state;
  }
}