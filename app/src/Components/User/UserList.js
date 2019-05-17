import React from 'react';

import { connect } from 'react-redux';
import { setUserPage, setUserRowsPerPage, setUserRowTotal, setUserSortColumn } from './../../actions/userList';

import UserRepository from './../../repository/UserRepository';
import ListContainer from '../ListTable/ListContainer';

class UserList extends React.Component {
  render() {
    const buttonConfig = [
      { 'function': 'edit', 'parameter': '/user', 'permissions': ['w_users'] },
      { 'function': 'delete', 'parameter': this._buildDeleteParam(), 'permissions': ['w_users'] }
    ];
    return <ListContainer
      buttons={buttonConfig}
      newLink={'/user/new'}
      repository={UserRepository}
      dataObjectName={'allUsers'}
      tableHeader={'Users'}
      {...this.props}
    />;
  }

  _buildExecuteParam() {
    return {
      'repository': UserRepository
    };
  }

  _buildDeleteParam() {
    return {
      'page': this.props.page,
      'rowTotal': this.props.rowTotal,
      'rowsPerPage': this.props.rowsPerPage,
      'setPage': this.props.setPage,
      'sortColumn': this.props.sortColumn,
      'usePagination': true,
      'repository': UserRepository
    };
  }
}

const mapStateToProps = (state) => ({
  'page': state.userPage,
  'rowsPerPage': state.userRowsPerPage,
  'rowTotal': state.userRowTotal,
  'sortColumn': state.userSortColumn
});

const mapDispatchToProps = (dispatch) => ({
  'setPage': (page) => dispatch(setUserPage(page)),
  'setRowsPerPage': (rowsPerPage) => dispatch(setUserRowsPerPage(rowsPerPage)),
  'setRowTotal': (rowTotal) => dispatch(setUserRowTotal(rowTotal)),
  'setSortColumn': (sortColumn) => dispatch(setUserSortColumn(sortColumn))
});

export default connect(mapStateToProps, mapDispatchToProps)(UserList);
