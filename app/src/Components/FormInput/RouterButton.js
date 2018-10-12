import React from 'react';
import { withRouter } from 'react-router-dom'
import PropTypes from 'prop-types';
import SimpleButton from './SimpleButton'

const RouterButton = withRouter(({history, targetLocation, disabled, label}) => (
  <SimpleButton
      type={targetLocation === 'back' ? 'cancel' : 'create'}
      disabled={disabled}
      label={label}
      variant='contained'
      onClick={() => {targetLocation === 'back' ? history.goBack() : history.replace(targetLocation)}}/>
))

export default RouterButton;

RouterButton.propTypes = {
  targetLocation: PropTypes.string.isRequired,
  disabled: PropTypes.bool.isRequired,
  label: PropTypes.string.isRequired,
};