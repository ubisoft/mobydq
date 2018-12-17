import React from 'react';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';

const SaveButton = ({
  onClick,
  disabled
}) => <Button
  type={'submit'}
  variant={'contained'}
  color={'secondary'}
  size={'small'}
  style={{ 'marginRight': '10px' }}
  onClick={onClick}
  disabled={disabled}
>
  <SaveIcon />
  Save
</Button>;

export default SaveButton;
