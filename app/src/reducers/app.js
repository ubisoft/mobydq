export function alertDialog(state = null, action) {
  switch (action.type) {
    case 'ALERT_DIALOG':
      return action.alertDialog;
    default:
      return state;
  }
}
