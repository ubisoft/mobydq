import React, { useState } from 'react';
import MaterialModal from '@material-ui/core/Modal';


export default function withModal(WrappedComponent) {
  return function wrappedWithModal(props) {
    const [isShown, setIsShown] = useState(false);
    const hide = () => setIsShown(false);
    const show = () => setIsShown(true);

    return <div>
      <WrappedComponent isModalOpen={isShown} showModal={show} {...props} />
      <MaterialModal
        open={isShown}
        onClose={hide}>
        <div style={{'width': '50%', 'height': '50%', 'backgroundColor': '#FFF' }}>Something</div>
      </MaterialModal>
    </div>;
  };
}
