import React from 'react';
import { ListTableCell } from './ListTableCell';
import createEditRowFunction from './ListRowButtons/EditRowButton';
import createDeleteRowButton from './ListRowButtons/DeleteRowButton';
import createExecuteRowButton from './ListRowButtons/ExecuteRowButton';


/**
 * Container component for TableRow Action Buttons
 *
 * @param buttons a list of buttons
 * @param value an id of the row element
 * #param button.parameter base_path for a predefined function or a custom function for a custom action
 *
 * Calls a Button component to render each button
 */

class ListTableRowButtons extends React.Component {
  render() {
    return <ListTableCell contents={this.props.buttons.map((button) => this._createButton(button))} />;
  }

  _createButton(button) {
    const recordId = this.props.value;
    switch (button.function) {
      case 'edit':
        return createEditRowFunction(button, recordId);
      case 'delete':
        return createDeleteRowButton(button, recordId);
      case 'execute':
        return createExecuteRowButton(button, recordId);
      default:
        return <React.Fragment key={`none_${recordId}`} />;
    }
  }
}

export default ListTableRowButtons;
