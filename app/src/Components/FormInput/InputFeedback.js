import React from 'react';

const InputFeedback = ({ error }) =>
  error ? (
    <div className="input-feedback">{error}</div>
  ) : null;

export default InputFeedback;