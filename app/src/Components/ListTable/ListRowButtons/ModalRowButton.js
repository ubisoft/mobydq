import React from 'react';
import { Link } from 'react-router-dom';
import IconButton from '@material-ui/core/IconButton';

import EditIcon from '@material-ui/icons/Edit';
import withModal from '../../../hoc/withModal';

const ModalButton = ({ button, recordId, showModal, setModalContent, closeModal }) => {
  return <IconButton color="secondary" onClick={() => onModalButtonClick(button, recordId, setModalContent, showModal, closeModal)}>
    {button.icon}
  </IconButton>;
}

function onModalButtonClick(button, recordId, setModalContent, showModal, closeModal) {
  setModalContent(button.modalContent(recordId, closeModal));
  showModal();
}

export default withModal(ModalButton);
