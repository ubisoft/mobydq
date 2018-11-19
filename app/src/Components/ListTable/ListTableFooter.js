import React from 'react';

import TableRow from '@material-ui/core/TableRow';
import TableFooter from '@material-ui/core/TableFooter';
import TablePagination from '@material-ui/core/TablePagination';
import TablePaginationActionsWrapped from './TablePaginationActions';

class ListTableFooter extends React.Component {
  constructor() {
    super();
    this.handleChangePage = this.handleChangePage.bind(this);
    this.handleChangeRowsPerPage = this.handleChangeRowsPerPage.bind(this);
  }

  render() {
    return <TableFooter>
      <TableRow>
        <TablePagination
          colSpan={10}
          count={this.props.params.rowTotal}
          rowsPerPage={this.props.params.rowsPerPage}
          page={this.props.params.page}
          onChangePage={this.handleChangePage}
          onChangeRowsPerPage={(event) => this.handleChangeRowsPerPage(event)}
          ActionsComponent={TablePaginationActionsWrapped}
        />
      </TableRow>
    </TableFooter>;
  }

  handleChangePage(page) {
    this.props.params.setPage(page);
  }

  handleChangeRowsPerPage(event) {
    this.props.params.setRowsPerPage(event.target.value);
  }
}

export default ListTableFooter;
