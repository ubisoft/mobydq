import React from 'react';

import { connect } from 'react-redux';

import ParameterRepository from './../../../repository/ParameterRepository';
import ListTable from '../../ListTable/ListTable';

class ParameterList extends React.Component {
  render() {
    const buttonConfig = [
      { 'function': 'edit', 'parameter': '/parameter' },
//      { 'function': 'delete', 'parameter': this._buildDeleteParam() }
    ];
    return <div>
      Indicator Parameters
      <ListTable
        data={this.props.data !== null ? this.props.data.nodes : []}
        buttons={buttonConfig}
        sortColumn='id'
        showFooter={false}
        useSort={false}
        {...this.props}
      />
    </div>
  }

  _buildDeleteParam() {
    return {
      'page': null,
      'rowTotal': null,
      'rowsPerPage': null,
      'setPage': null,
      'sortColumn': 'id',
      'repository': ParameterRepository
    };
  }
}


export default ParameterList;
