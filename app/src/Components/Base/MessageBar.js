import Snackbar from '@material-ui/core/Snackbar/Snackbar';
import React from 'react';

export const  MessageBar = ({ message, isOpen, setOpen }) => <Snackbar
  anchorOrigin={{
    'vertical': 'bottom',
    'horizontal': 'left'
  }}
  open={isOpen}
  autoHideDuration={5000}
  message={<span>{message}</span>}
  onClose={() => setOpen(false)}>
</Snackbar>;
