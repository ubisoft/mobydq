import React from 'react';

import { connect } from 'react-redux';

import ParameterRepository from './../../../repository/ParameterRepository';
import ListTable from '../../ListTable/ListTable';
import Button from '@material-ui/core/Button';
import withModal from '../../../hoc/withModal';
import { ParameterUpdateForm } from './ParameterUpdateForm';
import { EnhancedForm } from './../../Form/Form';
import EnhancedParameterForm from './ParameterForm';

import EditIcon from '@material-ui/icons/Edit';

const ParameterList = (props) => {
  const buttonConfig = [
      { 'function': 'modal', 'icon': <EditIcon/>, 'modalContent': _buildEditModalContent },
      { 'function': 'delete', 'parameter': _buildDeleteParam() }
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
    'page': 0,
    'rowTotal': 100,
    'rowsPerPage': 100,
    'setPage': null,
    'sortColumn': 'id',
    'usePagination': false,
    'repository': ParameterRepository
  };
}

function _buildEditModalContent(recordId, closeModal) {
  return <div style={{ 'backgroundColor': '#FFF', 'width': '750px', 'margin': '0 auto' }}><ParameterUpdateForm id={recordId} afterSave={closeModal}/></div>;
}

function _closeModal(props) {
  props.closeModal();
  window.location.reload();
}

export default withModal(ParameterList);
