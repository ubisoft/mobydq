import React, { useState } from 'react';
import MaterialModal from '@material-ui/core/Modal';


export default function withModal(WrappedComponent) {
  return function wrappedWithModal(props) {
    const [isShown, setIsShown] = useState(false);
    const [modalContent, setModalContent] = useState(<div style={{'width': '50%', 'height': '50%', 'backgroundColor': '#FFF' }}>a modal</div>)
    const hide = () => setIsShown(false);
    const show = () => setIsShown(true);

    return <div>
      <WrappedComponent isModalOpen={isShown} showModal={show} closeModal={hide} setModalContent={setModalContent} {...props} />
      <MaterialModal
        open={isShown}
        onClose={hide}>
        {modalContent}
      </MaterialModal>
    </div>;
  };
}
