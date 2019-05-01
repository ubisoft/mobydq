import React from 'react';
import IconButton from '@material-ui/core/IconButton';

import withModal from '../../../hoc/withModal';

const ModalButton = (props) => <IconButton
  color="secondary" onClick={() => onModalButtonClick(props)}>
  {props.button.icon}
</IconButton>;

function onModalButtonClick(props) {
  props.setModalContent(props.button.modalContent(props.recordId, props.closeModal));
  props.showModal();
}

export default withModal(ModalButton);
