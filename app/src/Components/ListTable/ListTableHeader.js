import React from 'react';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import Tooltip from '@material-ui/core/Tooltip';

/**
 * Component to build the list table header.
 * @param headerNames array of column names
 */
class ListTableHeader extends React.Component {
  _handleSortClick = (fieldName, isActive, direction) => {
    const newDirection = (isActive && direction === SORT_ORDER.DESCENDING) ? 'ASC' : 'DESC';
    this.props.params.setSortColumn(fieldName + '_' + newDirection);
  };

  /**
  * GraphQL uses FIELD_NAME format for defining the sort directives as opposed to camelCase in the field names.
  * This function is responsible for the necessary field name conversion
  **/
  _buildSortableHeaderCell(header, sortHeader, sortActive, sortDirection) {
    return header === 'Actions'
      ? <React.Fragment>{header}</React.Fragment>
      : <Tooltip
          title='Sort'
          placement={'bottom-start'}
          enterDelay={300}
        >
          <TableSortLabel
            active={sortActive}
            direction={sortDirection}
            onClick={() => this._handleSortClick(sortHeader, sortActive, sortDirection)}
          >
            {header}
          </TableSortLabel>
        </Tooltip>;
  }

  _buildHeaderCell(fieldName, sortField, sortDirection) {
    let header = fieldName;
    let sortHeader = '';
   if (header.length > 0) {
      header = header.charAt(0).toUpperCase() + header.slice(1);
      sortHeader = header.match(/[A-Z][a-z]+/ug).join('_').toUpperCase();
      header = header.match(/[A-Z][a-z]+/ug).join(' ');
    }
    sortDirection = (sortField && sortHeader === sortField) ? sortDirection.toLowerCase() : SORT_ORDER.DESCENDING;
    const sortActive = sortField && sortHeader === sortField && fieldName !== 'Actions';
    return (
      <TableCell
        key={header}
      >
        {this._buildSortableHeaderCell(header, sortHeader, sortActive, sortDirection)}
      </TableCell>
    );
  }

  _buildHeader(headerFields) {
    // Add "Actions column
    const sortField = this.props.params.sortColumn;
    const allHeaderFields = headerFields.concat(['Actions']);
    //sort field is either null or FIELD_NAME_ASC/DESC
    const sortFieldName = sortField === null ? null : sortField.substring(0, sortField.lastIndexOf("_"));
    const sortDirection = sortField === null ? null : sortField.substring(sortField.lastIndexOf("_") + 1);
    return (
      <TableHead>
        <TableRow>
          {allHeaderFields.map((fieldName) => this._buildHeaderCell(fieldName, sortFieldName, sortDirection))}
        </TableRow>
      </TableHead>
    );
  }

  render() {
    return this._buildHeader(this.props.headerNames);
  }
}

const SORT_ORDER = {
    'DESCENDING': 'desc',
    'ASCENDING': 'asc'
}

export default ListTableHeader;


