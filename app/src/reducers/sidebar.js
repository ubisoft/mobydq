export function sidebarIsOpen(state=true, action) {
  switch (action.type) {
    case 'SIDEBAR_IS_OPEN':
      return action.isOpen;
    default:
      return state;
  }
};