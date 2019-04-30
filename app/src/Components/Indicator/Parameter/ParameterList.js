import React from 'react';

import { connect } from 'react-redux';

import ParameterRepository from './../../../repository/ParameterRepository';
import ListTable from '../../ListTable/ListTable';
import Button from '@material-ui/core/Button';
import withModal from '../../../hoc/withModal';
import { ParameterUpdateForm } from './ParameterUpdateForm';
import { EnhancedForm } from './../../Form/Form';
import EnhancedParameterForm from './ParameterForm';

const ParameterList = (props) => {
  const buttonConfig = [
    { 'function': 'edit', 'parameter': '/parameter' }
    ];
    const createFormModalContent = <div style={{ 'backgroundColor': '#FFF', 'width': '750px', 'margin': '0 auto' }}>
     <EnhancedForm ComponentRepository={ParameterRepository} FormComponent={EnhancedParameterForm}
       title="Create Parameter" initialFieldValues={null} indicatorId={props.indicatorId} afterSave={() => _closeModal(props)}/>
    </div>;
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
            props.setModalContent(createFormModalContent);
//            this.props.setModalContent( <div style={{ 'backgroundColor': '#FFF', 'width': '750px', 'margin': '0 auto' }}><ParameterUpdateForm id={}/></div>)
            props.showModal();
          } }
          disabled={false}
        >
          Add parameter
        </Button>
      </div>
      <ListTable
        data={props.data !== null ? props.data.nodes : []}
        buttons={buttonConfig}
        sortColumn="id"
        showFooter={false}
        useSort={false}
        {...props}
      />
    </div>;
  };

function _buildDeleteParam() {
  return {
    'page': null,
    'rowTotal': null,
    'rowsPerPage': null,
    'setPage': null,
    'sortColumn': 'id',
    'repository': ParameterRepository
  };
}

function _closeModal(props) {
  props.closeModal();
  window.location.reload();
}

export default withModal(ParameterList);
