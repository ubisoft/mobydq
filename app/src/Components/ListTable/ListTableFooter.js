import React from 'react';
import { connect } from 'react-redux';
import { setPage, setRowsPerPage } from './../../actions/listTable';

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import TableRow from '@material-ui/core/TableRow';
import IconButton from '@material-ui/core/IconButton';
import FirstPageIcon from '@material-ui/icons/FirstPage';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import LastPageIcon from '@material-ui/icons/LastPage';


import TableFooter from '@material-ui/core/TableFooter';
import TablePagination from '@material-ui/core/TablePagination';

const actionsStyles = theme => ({
  root: {
    flexShrink: 0,
    color: theme.palette.text.secondary,
    marginLeft: theme.spacing.unit * 2.5,
  },
});

class TablePaginationActions extends React.Component {

  handleFirstPageButtonClick = () => {
    this.props.onChangePage(0);
  };

  handleBackButtonClick = () => {
    this.props.onChangePage(this.props.page - 1);
  };

  handleNextButtonClick = () => {
    this.props.onChangePage(this.props.page + 1);
  };

  handleLastPageButtonClick = () => {
    this.props.onChangePage(
      Math.max(0, Math.ceil(this.props.count / this.props.rowsPerPage) - 1),
    );
  };

  render() {
    const { classes, theme } = this.props;
    let count = this.props.count;
    let page = this.props.page;
    let rowsPerPage = this.props.rowsPerPage;
    return (
      <div className={classes.root}>
        <IconButton
          onClick={this.handleFirstPageButtonClick}
          disabled={page === 0}
          aria-label="First Page"
        >
          {theme.direction === 'rtl' ? <LastPageIcon /> : <FirstPageIcon />}
        </IconButton>
        <IconButton
          onClick={this.handleBackButtonClick}
          disabled={page === 0}
          aria-label="Previous Page"
        >
          {theme.direction === 'rtl' ? <KeyboardArrowRight /> : <KeyboardArrowLeft />}
        </IconButton>
        <IconButton
          onClick={this.handleNextButtonClick}
          disabled={page >= Math.ceil(count / rowsPerPage) - 1}
          aria-label="Next Page"
        >
          {theme.direction === 'rtl' ? <KeyboardArrowLeft /> : <KeyboardArrowRight />}
        </IconButton>
        <IconButton
          onClick={this.handleLastPageButtonClick}
          disabled={page >= Math.ceil(count / rowsPerPage) - 1}
          aria-label="Last Page"
        >
          {theme.direction === 'rtl' ? <FirstPageIcon /> : <LastPageIcon />}
        </IconButton>
      </div>
    );
  }
}

TablePaginationActions.propTypes = {
  classes: PropTypes.object.isRequired,
  onChangePage: PropTypes.func.isRequired,
  theme: PropTypes.object.isRequired,
};

const TablePaginationActionsWrapped = withStyles(actionsStyles, { withTheme: true })(
  TablePaginationActions,
);

class ListTableFooter extends React.Component {
  constructor(){
    super();
    this.handleChangePage = this.handleChangePage.bind(this);
    this.handleChangeRowsPerPage = this.handleChangeRowsPerPage.bind(this);
  }

  render() {
    return (<TableFooter>
      <TableRow>
        <TablePagination
          colSpan={3}
          count={this.props.rowTotal}
          rowsPerPage={this.props.rowsPerPage}
          page={this.props.page}
          onChangePage={this.handleChangePage}
          onChangeRowsPerPage={(event) => this.handleChangeRowsPerPage(event)}
          ActionsComponent={TablePaginationActionsWrapped}
        />
      </TableRow>
    </TableFooter>);
  }

  handleChangePage(page) {
    this.props.setPage(page);
  };

  handleChangeRowsPerPage(event) {
    this.props.setRowsPerPage(event.target.value);
  };

}



const mapStateToProps = (state) => ({
  'page': state.page,
  'rowsPerPage': state.rowsPerPage,
  'rowTotal': state.rowTotal
});

const mapDispatchToProps = (dispatch) => ({
  'setPage': (page) => dispatch(setPage(page)),
  'setRowsPerPage': (rowsPerPage) => dispatch(setRowsPerPage(rowsPerPage)),
});

export default connect(mapStateToProps, mapDispatchToProps)(ListTableFooter);
