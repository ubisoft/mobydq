import React from 'react';
import EditIcon from '@material-ui/icons/Edit';
import { Link } from 'react-router-dom';
import IconButton from '@material-ui/core/IconButton';


export default function createEditRowFunction(button, recordId, disabled) {
  return (
    <IconButton key={`edit_${recordId}`} component={Link} to={`${button.parameter}/edit/${recordId}`} color="secondary" disabled={disabled}>
      <EditIcon />
    </IconButton>
  );
}
