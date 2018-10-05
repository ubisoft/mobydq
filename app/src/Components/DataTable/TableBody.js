import React from 'react';
import {styles} from '../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import TableRow from './TableRow'

class DataTableBody extends React.Component {
  render() {
    return (
      <React.Fragment>
        {this.props.tableContent.map((row) => (
          <TableRow buttons={this.props.buttons} key={row['id']} rowData={Object.values(row)}/>
        ))}
      </React.Fragment>
    )
  }
}

export default withStyles(styles)(DataTableBody);
