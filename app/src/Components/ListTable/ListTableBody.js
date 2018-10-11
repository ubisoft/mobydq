import React from 'react';
import {styles} from '../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import TableBody from '@material-ui/core/TableBody';
import { ListTableRow } from './ListTableRow';

/**
 * Container component for the list table data
 *
 * @param content - array of objects to be displayed in the list.
 * @param contentColumnList - array of table column names (required to iterate the object)
 * @param (Optional) buttons - list of buttons to be shown in Action column
 *
 * Component calls DataTableRow container component
 */

export const ListTableBody = ({content, contentColumnList, buttons}) => {
  return (
    <TableBody>
      {
        content.map((row) => (
          <ListTableRow buttons={buttons} key={row.id} rowData={row} rowColumns={contentColumnList}/>
        ))
      }
    </TableBody>
  );
}

export default withStyles(styles)(ListTableBody);
