import React from 'react';
import PropTypes from 'prop-types'
import {styles} from '../../styles/baseStyles';
import {withStyles} from '@material-ui/core/styles';
import TableCell from '@material-ui/core/TableCell';
import DoneIcon from '@material-ui/icons/Done';
import ClearIcon from '@material-ui/icons/Clear';
import { TableRow as MTableRow } from '@material-ui/core/TableRow';
import TableRowButtons from './TableRowButtons';
import Button from '@material-ui/core/Button';
import Style from '../../index.css';



class TableRow extends React.Component
{
  _isFlagActive(flag) {
    if(typeof(flag) === "boolean") {
      if (flag) {
        return <DoneIcon color="primary"/>;
      }
      return <ClearIcon color="error"/>
      }
  }
  _renderDataRow(rowData) {
    return rowData.map((value) => (
      <TableCell key={value}>{value} {this._isFlagActive(value)}</TableCell>
    ));
  }


  render() {
    if (this.props.rowData === null || this.props.buttons.rowData !== Array) {
      return (<React.Fragment/>);
    }
    return(
      <MTableRow>
        {this._renderDataRow(this.props.rowData)}
        <TableRowButtons buttons={this.props.buttons} value={this.props.rowData[0]}/>
      </MTableRow>
    );
  }
}

export default withStyles(styles)(TableRow);

TableRow.defaultProps = {
  rowData: [],
  buttons: [],
};

TableRow.propTypes = {
  buttons: PropTypes.array,
  rowData: PropTypes.array.isRequired
}