
export function setMessageBarMessage(str) {
  return {
    'type': 'MESSAGE_BAR_MESSAGE',
    'message': str
  };
}

export function setMessageBarOpen(bool) {
  return {
    'type': 'MESSAGE_BAR_IS_OPEN',
    'messageBarIsOpen': bool
  };
}
