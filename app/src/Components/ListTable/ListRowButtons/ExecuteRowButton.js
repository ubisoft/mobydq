import React from 'react';
import { connect } from 'react-redux';
import { Mutation } from 'react-apollo';
import IconButton from '@material-ui/core/IconButton';
import PlayArrow from '@material-ui/icons/PlayArrow';

import { setMessageBarMessage, setMessageBarOpen } from '../../../actions/messageBar';

class ExecuteRowButton extends React.Component {
  execute = (func) => {
    func();
    this.props.setMessageBarOpen(true);
  }

  render() {
    return <Mutation
      mutation={this.props.parameter.repository.execute()}
      variables={{ 'id': this.props.recordId }}>
      {(executeFunc, params) => {
        const { loading, error, called, data } = params;
        if (loading) {
          return <p>Loading...</p>;
        }

        if (error) {
          return <p>Error...</p>;
        }

        if (called && data) {
          const responseData = data.executeBatch.batch;
          if (responseData.id !== this.props.currentBatchId) {
            this.props.setMessageBarMessage(`Batch ${responseData.id}: ${responseData.status}`);
          }
        }

        return (
          <React.Fragment>
            <IconButton key={`execute_${this.props.recordId}`} onClick={() => this.execute(executeFunc)} color="secondary">
              <PlayArrow />
            </IconButton>
          </React.Fragment>
        );
      }}
    </Mutation>;
  }
}

const mapStateToProps = (state) => ({
  'messageBarMessage': state.messageBarMessage
});

const mapDispatchToProps = (dispatch) => (
  {
    'setMessageBarMessage': (message) => dispatch(setMessageBarMessage(message)),
    'setMessageBarOpen': (open) => dispatch(setMessageBarOpen(open))
  }
);

const VisibleExecuteRowButton = connect(mapStateToProps, mapDispatchToProps)(ExecuteRowButton);

export default function createExecuteRowButton(button, recordId) {
  return <VisibleExecuteRowButton
    key={`execute_${recordId}`}
    parameter={button.parameter}
    recordId={recordId}>
  </VisibleExecuteRowButton>;
}
