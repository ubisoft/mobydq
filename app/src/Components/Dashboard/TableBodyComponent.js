import React from 'react';
import {styles} from './../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import TableBodyRowComponent from '../Dashboard/TableBodyRowComponent'

class TableBodyComponent extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            tableContent: this.props.tableContent,
        }
    }

    render() {
        return (
            <React.Fragment>
                {this.props.tableContent.map((row) => (
                        <TableBodyRowComponent buttons={this.props.buttons} key={row['id']} rowData={Object.values(row)}/>
                ))}
            </React.Fragment>
        )
    }
}

export default withStyles(styles)(TableBodyComponent);
