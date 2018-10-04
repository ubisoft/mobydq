import React from 'react';
import {styles} from './../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import TableCell from '@material-ui/core/TableCell';
import DoneIcon from '@material-ui/icons/Done';
import ClearIcon from '@material-ui/icons/Clear';
import TableRow from '@material-ui/core/TableRow'


class TableBodyRowComponent extends React.Component
{
    constructor(props)
    {
        super(props);

        this.state = {
            rowData: this.props.rowData,
        }
    }

        isFlagActive(flag) {
        if(typeof(flag) === "boolean") {
            if (flag) {
                return <DoneIcon color="primary"/>;
            }
            return <ClearIcon color="error"/>
        }
    }


    render()
    {
        let isFlagActiveFunction = this.isFlagActive;
        return(
            <TableRow>
                {this.state.rowData.map((value) => (
                    <TableCell key={value}>{value} {isFlagActiveFunction(value)}</TableCell>
                ))}
            </TableRow>
        )
    }
}

export default withStyles(styles)(TableBodyRowComponent);