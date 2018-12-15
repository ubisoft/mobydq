import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import PlayArrow from '@material-ui/icons/PlayArrow';

const ExecuteButton = ({
  onClick,
  disabled
}) => <Button
  type={'execute'}
  variant={'contained'}
  color={'secondary'}
  size={'small'}
  style={{ 'marginRight':'10px'}}
  onClick={onClick}
  disabled={disabled}
  >
  <PlayArrow />
  Execute
</Button>;

export default ExecuteButton;
