import React from 'react';
import {styles} from './../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'

class TableHeaderComponent extends React.Component {

    constructor (props) {

        super(props);

        this.state = {
            headerNames: this.props.headerNames,
        };

    }


    render() {
        let a = 0;
        return(
            <TableRow>
                {this.state.headerNames.map((item) => (
                    <TableCell key={item}>{item}</TableCell>
                ))
                }
            </TableRow>
        )
    }
}

export default withStyles(styles)(TableHeaderComponent);

