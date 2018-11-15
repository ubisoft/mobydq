import React from 'react';

import { connect } from 'react-redux';
import { setDataSourcePage, setDataSourceRowsPerPage, setDataSourceRowTotal, setDataSourceSortColumn } from './../../actions/dataSourceList';

import DataSourceRepository from './../../repository/DataSourceRepository';
import ListContainer from '../ListTable/ListContainer';

class DataSourceList extends React.Component {
  render() {
    const buttonConfig = [
      { 'function': 'edit', 'parameter': '/data-source' },
      { 'function': 'delete', 'parameter': this._buildDeleteParam() }
    ];
    return <ListContainer
      buttons={buttonConfig}
      newLink='/data-source/new'
      repository={DataSourceRepository}
      dataObjectName='allDataSources'
      tableHeader='Data Sources'
      {...this.props}
    />;
  }

  _buildDeleteParam() {
    return {
      'page': this.props.page,
      'rowTotal': this.props.rowTotal,
      'rowsPerPage': this.props.rowsPerPage,
      'setPage': this.props.setPage,
      'repository': DataSourceRepository
    };
  }
}

const mapStateToProps = (state) => ({
  'page': state.dataSourcePage,
  'rowsPerPage': state.dataSourceRowsPerPage,
  'rowTotal': state.dataSourceRowTotal,
  'sortColumn': state.dataSourceSortColumn
});

const mapDispatchToProps = (dispatch) => ({
  'setPage': (page) => dispatch(setDataSourcePage(page)),
  'setRowsPerPage': (rowsPerPage) => dispatch(setDataSourceRowsPerPage(rowsPerPage)),
  'setRowTotal': (rowTotal) => dispatch(setDataSourceRowTotal(rowTotal)),
  'setSortColumn': (sortColumn) => dispatch(setDataSourceSortColumn(sortColumn))
});

export default connect(mapStateToProps, mapDispatchToProps)(DataSourceList);
