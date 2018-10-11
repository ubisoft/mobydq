import React from 'react';
import TableCell from '@material-ui/core/TableCell';

/**
 * Table cell  presentational component
 *
 * @param contents - table cell contents.
 * @param key - Table cell key
 *
 */

export const ListTableCell = ({contents}) => {
  return (
    <TableCell>{contents}</TableCell>
  );
}

export default ListTableCell
