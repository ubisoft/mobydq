import React from 'react';
import { styles } from '../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Table from '@material-ui/core/Table';
import ListTableHeader from './ListTableHeader';
import ListTableFooter from './ListTableFooter';
import ListTableBody from './ListTableBody';

/**
 * Data model agnostic list table factory for the List view tables.
 * @param data - array of object data to be displayed in the list. The objects must have id field. Since we use
 * postgraphile, last element (__typename) is to be ignored.
 *
 * @param (Optional) buttons - list of buttons to be shown in Action column
 *
 * Calls on TableHeader and DataTableBody components
 */
class ListTable extends React.Component {
  _buildTableFieldNames() {
    const tableFieldNames = Object.keys(this.props.data[0]);
    // Remove redundant element __typename
    tableFieldNames.pop();
    return tableFieldNames;
  }

  render() {
    // Check if correct data prop is passed, otherwise render empty.
    if (this.props.data === null || !Array.isArray(this.props.data) || this.props.data.length === 0) {
      return <React.Fragment/>;
    }

    const headerNames = this._buildTableFieldNames();
    const content = this.props.data;
    return (
      <Table>
        <ListTableHeader headerNames={headerNames}/>
        <ListTableBody buttons={this.props.buttons} content={content} contentColumnList={headerNames}/>
        <ListTableFooter params={this.props.footerParams}/>
      </Table>
    );
  }
}


ListTable.propTypes = {
  'data': PropTypes.array.isRequired
};

ListTable.defaultProps = {
  'buttons': []
};

export default withStyles(styles)(ListTable);
