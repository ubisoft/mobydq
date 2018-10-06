import React from 'react';
import {styles} from '../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import DataTableRow from './TableRow'

class DataTableBody extends React.Component {
  render() {
    return (
      <React.Fragment>
        {
          this.props.content.map((row) => (
            <DataTableRow buttons={this.props.buttons} key={row[0]} rowContent={row}/>
          ))
        }
      </React.Fragment>
    )
  }
}

export default withStyles(styles)(DataTableBody);
