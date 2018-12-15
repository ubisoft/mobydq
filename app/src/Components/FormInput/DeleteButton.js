import React from 'react';
import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';

const DeleteButton = ({
  onClick,
  disabled
}) => <Button
  type={'submit'}
  variant={'outlined'}
  size={'small'}
  style={{ 'marginRight':'10px'}}
  onClick={onClick}
  disabled={disabled}
  >
  Delete
  <DeleteIcon />
</Button>;

export default DeleteButton;
