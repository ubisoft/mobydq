import React from 'react';
import MaterialModal from '@material-ui/core/Modal';


export default function Modal(props) {
  const [isShown, setIsShown] = useState(props.isShown);
  const hide = () => setIsShown(false);
  const show = () => setIsShown(true);

  return <MaterialModal
    open={isShown}
    onClose={hide}>
        Something
  </MaterialModal>;
}