import React from 'react';
import {styles} from '../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import {ListTableCell} from './ListTableCell';

/**
 * Component to build the list table header.
 * @param headerNames array of column names
 */
class ListTableHeader extends React.Component {
  _buildHeaderCell(fieldName) {
    if (fieldName.length > 0) {
      fieldName = fieldName.charAt(0).toUpperCase() + fieldName.slice(1);
      fieldName = fieldName.match(/[A-Z][a-z]+/g).join(' ');
    }
    return (
      <ListTableCell key={fieldName} contents={fieldName}/>
    )
  }

  _addActionsColumn(headerFields) {
    //add "Actions column
    headerFields.push('Actions');
    return headerFields;
  }

  _buildHeader(headerFields) {
    headerFields = this._addActionsColumn(headerFields);
    return (
      <TableHead>
        <TableRow>
          {headerFields.map((fieldName) => (this._buildHeaderCell(fieldName)))}
        </TableRow>
      </TableHead>
    );
  }

  render() {
    //make a deep copy to not modify the props data
    let headerFields = this.props.headerNames.slice(0);
    return (this._buildHeader(headerFields));
  }
}

export default ListTableHeader;

