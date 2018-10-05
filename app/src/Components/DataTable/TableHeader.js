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

  _addActionsColumn(headerFieldNames) {
    headerFieldNames.push('Actions');
    return headerFieldNames;
  }

  _buildHeader(headerFieldNames) {
    headerFieldNames = this._addActionsColumn(headerFieldNames);
    return (
      <TableRow>
        {headerFieldNames.map((fieldName) => (this._buildHeaderCell(fieldName)))}
      </TableRow>
    );
  }

  render() {
    return (this._buildHeader(this.props.headerNames));
  }
}

export default withStyles(styles)(TableHeader);

