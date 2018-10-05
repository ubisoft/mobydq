import React from 'react';
import {styles} from '../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import TableRow from './TableRow'

class DataTableBody extends React.Component {
  render() {
    return (
      <React.Fragment>
        {
          this.props.content.map((row) => (
            <TableRow buttons={this.props.buttons} key={row[0]} rowData={row}/>
          ))
        }
      </React.Fragment>
    )
  }
}

export default withStyles(styles)(DataTableBody);
