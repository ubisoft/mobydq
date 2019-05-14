import React from 'react';
import { ListTableCell } from './ListTableCell';
import createEditRowFunction from './ListRowButtons/EditRowButton';
import ModalButton from './ListRowButtons/ModalRowButton';
import createDeleteRowButton from './ListRowButtons/DeleteRowButton';
import createExecuteRowButton from './ListRowButtons/ExecuteRowButton';
import { isAuthenticated } from '../Base/PrivateRoute';


/**
 * Container component for TableRow Action Buttons
 *
 * @param buttons a list of buttons
 * @param value an id of the row element
 * #param button.parameter base_path for a predefined function or a custom function for a custom action
 *
 * Calls a Button component to render each button
 */

function ListTableRowButtons(props) {
  return <ListTableCell contents={props.buttons.map((button) => _createButton(button, props.value))}/>;
}

function _createButton(button, recordId) {
  // If permissions are set, it should only display them if the user fulfils the requirements.
  if (button.permissions) {
    const disableButton = !isAuthenticated(button);
    switch (button.function) {
      case 'edit':
        return createEditRowFunction(button, recordId, disableButton);
      case 'modal':
        return <ModalButton key={`modal_${recordId}`} button={button} recordId={recordId} disabled={disableButton}/>;
      case 'delete':
        return createDeleteRowButton(button, recordId, disableButton);
      case 'execute':
        return createExecuteRowButton(button, recordId, disableButton);
      default:
        return <React.Fragment key={`none_${recordId}`}/>;
    }
  } else {
    switch (button.function) {
      case 'edit':
        return createEditRowFunction(button, recordId);
      case 'modal':
        return <ModalButton key={`modal_${recordId}`} button={button} recordId={recordId}/>;
      case 'delete':
        return createDeleteRowButton(button, recordId);
      case 'execute':
        return createExecuteRowButton(button, recordId);
      default:
        return <React.Fragment key={`none_${recordId}`}/>;
    }
  }
}

export default ListTableRowButtons;
