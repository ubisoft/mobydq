import React from 'react';

import { connect } from 'react-redux';
import { setIndicatorPage, setIndicatorRowsPerPage, setIndicatorRowTotal, setIndicatorSortColumn } from './../../actions/indicatorList';

import IndicatorRepository from './../../repository/IndicatorRepository';
import ListContainer from '../ListTable/ListContainer';

class IndicatorList extends React.Component {
  render() {
    const buttonConfig = [
      { 'function': 'edit', 'parameter': '/indicator' },
      { 'function': 'delete', 'parameter': this._buildDeleteParam() }
    ];
    return <ListContainer
      buttons={buttonConfig}
      newLink={'/indicator/new'}
      repository={IndicatorRepository}
      dataObjectName={'allIndicators'}
      tableHeader={'Indicators'}
      {...this.props}
    />;
  }

  _buildDeleteParam() {
    return {
      'page': this.props.page,
      'rowTotal': this.props.rowTotal,
      'rowsPerPage': this.props.rowsPerPage,
      'setPage': this.props.setPage,
      'sortColumn': this.props.sortColumn,
      'usePagination': true,
      'repository': IndicatorRepository
    };
  }
}

const mapStateToProps = (state) => ({
  'page': state.indicatorPage,
  'rowsPerPage': state.indicatorRowsPerPage,
  'rowTotal': state.indicatorRowTotal,
  'sortColumn': state.indicatorSortColumn
});

const mapDispatchToProps = (dispatch) => ({
  'setPage': (page) => dispatch(setIndicatorPage(page)),
  'setRowsPerPage': (rowsPerPage) => dispatch(setIndicatorRowsPerPage(rowsPerPage)),
  'setRowTotal': (rowTotal) => dispatch(setIndicatorRowTotal(rowTotal)),
  'setSortColumn': (sortColumn) => dispatch(setIndicatorSortColumn(sortColumn))
});

export default connect(mapStateToProps, mapDispatchToProps)(IndicatorList);
