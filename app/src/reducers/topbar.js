export function userMenuAnchor(state = null, action) {
  switch (action.type) {
    case 'USER_MENU_ANCHOR':
      return action.userMenuAnchor;
    default:
      return state;
  }
}
