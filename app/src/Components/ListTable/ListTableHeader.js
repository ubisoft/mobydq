import React from 'react';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { ListTableCell } from './ListTableCell';

/**
 * Component to build the list table header.
 * @param headerNames array of column names
 */
class ListTableHeader extends React.Component {
  _buildHeaderCell(fieldName) {
    let header = fieldName;
    if (header.length > 0) {
      header = header.charAt(0).toUpperCase() + header.slice(1);
      header = header.match(/[A-Z][a-z]+/ug).join(' ');
    }
    return (
      <ListTableCell key={header} contents={header} />
    );
  }

  _buildHeader(headerFields) {
    // Add "Actions column
    const allHeaderFields = headerFields.concat(['Actions']);
    return (
      <TableHead>
        <TableRow>
          {allHeaderFields.map((fieldName) => this._buildHeaderCell(fieldName))}
        </TableRow>
      </TableHead>
    );
  }

  render() {
    return this._buildHeader(this.props.headerNames);
  }
}

export default ListTableHeader;
