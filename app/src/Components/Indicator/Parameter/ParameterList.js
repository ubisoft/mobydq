import React from 'react';

import { connect } from 'react-redux';

import ParameterRepository from './../../../repository/ParameterRepository';
import ListTable from '../../ListTable/ListTable';
import Button from '@material-ui/core/Button';
import withModal from '../../hoc/withModal';

class ParameterList extends React.Component {
  render() {
    console.log(this.props)
    const buttonConfig = [
      { 'function': 'edit', 'parameter': '/parameter' }
      //      { 'function': 'delete', 'parameter': this._buildDeleteParam() }
    ];
    return <div>
      <div style={{ 'display': 'flex', 'flexDirection': 'row' }}>
        <div>Indicator Parameters</div>
        <Button
          type={'submit'}
          variant={'contained'}
          color={'secondary'}
          size={'small'}
          style={{ 'marginRight': '10px', 'marginLeft': '10px' }}
          onClick={() => {
            this.props.showModal();
          } }
          disabled={false}
        >
          Add parameter
        </Button>
      </div>
      <ListTable
        data={this.props.data !== null ? this.props.data.nodes : []}
        buttons={buttonConfig}
        sortColumn="id"
        showFooter={false}
        useSort={false}
        {...this.props}
      />
    </div>;
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


export default withModal(ParameterList);
