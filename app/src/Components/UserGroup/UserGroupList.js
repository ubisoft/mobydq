import React from 'react';

import { connect } from 'react-redux';
import { setUserGroupPage, setUserGroupRowsPerPage, setUserGroupRowTotal, setUserGroupSortColumn } from './../../actions/userGroupList';

import UserGroupRepository from './../../repository/UserGroupRepository';
import ListContainer from '../ListTable/ListContainer';

class UserGroupList extends React.Component {
  render() {
    const buttonConfig = [
      { 'function': 'edit', 'parameter': '/user-group' },
      { 'function': 'delete', 'parameter': this._buildDeleteParam() }
    ];
    return <ListContainer
      buttons={buttonConfig}
      newLink={'/user-group/new'}
      repository={UserGroupRepository}
      dataObjectName={'allUserGroups'}
      tableHeader={'User Groups'}
      {...this.props}
    />;
  }

  _buildExecuteParam() {
    return {
      'repository': UserGroupRepository
    };
  }

  _buildDeleteParam() {
    return {
      'page': this.props.page,
      'rowTotal': this.props.rowTotal,
      'rowsPerPage': this.props.rowsPerPage,
      'setPage': this.props.setPage,
      'sortColumn': this.props.sortColumn,
      'repository': UserGroupRepository
    };
  }
}

const mapStateToProps = (state) => ({
  'page': state.userGroupPage,
  'rowsPerPage': state.userGroupRowsPerPage,
  'rowTotal': state.userGroupRowTotal,
  'sortColumn': state.userGroupSortColumn
});

const mapDispatchToProps = (dispatch) => ({
  'setPage': (page) => dispatch(setUserGroupPage(page)),
  'setRowsPerPage': (rowsPerPage) => dispatch(setUserGroupRowsPerPage(rowsPerPage)),
  'setRowTotal': (rowTotal) => dispatch(setUserGroupRowTotal(rowTotal)),
  'setSortColumn': (sortColumn) => dispatch(setUserGroupSortColumn(sortColumn))
});

export default connect(mapStateToProps, mapDispatchToProps)(UserGroupList);
