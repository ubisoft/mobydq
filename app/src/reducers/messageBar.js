export function messageBarMessage(state = '', action) {
  switch (action.type) {
    case 'MESSAGE_BAR_MESSAGE':
      return action.message;
    default:
      return state;
  }
}

export function messageBarIsOpen(state = false, action) {
  switch (action.type) {
    case 'MESSAGE_BAR_IS_OPEN':
      return action.messageBarIsOpen;
    default:
      return state;
  }
}