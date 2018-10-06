import React from 'react';
import {styles} from '../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';

class TableHeader extends React.Component {
    _buildHeaderCell(fieldName) {
    fieldName = fieldName.charAt(0).toUpperCase() + fieldName.slice(1);
    fieldName = fieldName.match(/[A-Z][a-z]+/g).join(" ");
    return (
      <TableCell key={fieldName}>{fieldName}</TableCell>
    )
  }

  _addActionsColumn(headerFields) {
    headerFields.push('Actions');
    return headerFields;
  }

  _buildHeader(headerFields) {
    headerFields = this._addActionsColumn(headerFields);
    return (
      <TableRow>
        {headerFields.map((fieldName) => (this._buildHeaderCell(fieldName)))}
      </TableRow>
    );
  }

  render() {
    let headerFields = this.props.headerNames.slice(0)
    return (this._buildHeader(headerFields));
  }
}

export default withStyles(styles)(TableHeader);

