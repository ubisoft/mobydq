import React from 'react';

import { connect } from 'react-redux';
import { setIndicatorGroupPage, setIndicatorGroupRowsPerPage, setIndicatorGroupRowTotal, setIndicatorGroupSortColumn } from './../../actions/indicatorGroupList';

import IndicatorGroupRepository from './../../repository/IndicatorGroupRepository';
import ListContainer from '../ListTable/ListContainer';

class IndicatorGroupList extends React.Component {
  render() {
    const buttonConfig = [
      { 'function': 'execute', 'parameter': this._buildExecuteParam(), 'permissions': [/* TBD for a user group*/] },
      { 'function': 'edit', 'parameter': '/indicator-group', 'permissions': ['w_indicator_groups'] },
      { 'function': 'delete', 'parameter': this._buildDeleteParam(), 'permissions': ['w_indicator_groups'] }
    ];
    return <ListContainer
      buttons={buttonConfig}
      newLink={'/indicator-group/new'}
      repository={IndicatorGroupRepository}
      dataObjectName={'allIndicatorGroups'}
      tableHeader={'Indicator Groups'}
      {...this.props}
    />;
  }

  _buildExecuteParam() {
    return {
      'repository': IndicatorGroupRepository
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
      'repository': IndicatorGroupRepository
    };
  }
}

const mapStateToProps = (state) => ({
  'page': state.indicatorGroupPage,
  'rowsPerPage': state.indicatorGroupRowsPerPage,
  'rowTotal': state.indicatorGroupRowTotal,
  'sortColumn': state.indicatorGroupSortColumn
});

const mapDispatchToProps = (dispatch) => ({
  'setPage': (page) => dispatch(setIndicatorGroupPage(page)),
  'setRowsPerPage': (rowsPerPage) => dispatch(setIndicatorGroupRowsPerPage(rowsPerPage)),
  'setRowTotal': (rowTotal) => dispatch(setIndicatorGroupRowTotal(rowTotal)),
  'setSortColumn': (sortColumn) => dispatch(setIndicatorGroupSortColumn(sortColumn))
});

export default connect(mapStateToProps, mapDispatchToProps)(IndicatorGroupList);
