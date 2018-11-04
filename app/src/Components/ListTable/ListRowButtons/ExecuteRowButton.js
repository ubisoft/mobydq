import React from 'react';
import { connect } from 'react-redux';
import { Mutation } from 'react-apollo';
import IconButton from '@material-ui/core/IconButton';
import PlayArrow from '@material-ui/icons/PlayArrow';
import Snackbar from '@material-ui/core/Snackbar';
import { setIndicatorGroupCurrentBatchId, setIndicatorGroupOpen, setIndicatorGroupMessage } from '../../../actions/indicatorGroupList';


class ExecuteRowButton extends React.Component {

  execute = (func) => {
    func();
    this.props.setOpen(true);
  }

  render() {
    return (<Mutation
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
          const responseData = data['executeBatch']['batch'];
          if (responseData.id !== this.props.currentBatchId) {
            this.props.setMessage(`Batch ${responseData.id}: ${responseData.status}`);
            this.props.setCurrentBatchId(responseData.id);
          }
        }

        return (
          <div>
            <Snackbar
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left'
              }}
              open={this.props.open}
              autoHideDuration={5000}
              message={<span>{this.props.message}</span>}
              onClose={() => this.props.setOpen(false)}>
            </Snackbar>
            <IconButton key={`execute_${this.props.recordId}`} onClick={() => this.execute(executeFunc)} color="primary">
              <PlayArrow />
            </IconButton>
          </div>);
      }}
    </Mutation>);
  }
}

const mapStateToProps = (state) => {
  return ({
    'message': state.indicatorGroupMessage,
    'open': state.indicatorGroupOpen,
    'currentBatchId': state.indicatorGroupCurrentBatchId
  });
}

const mapDispatchToProps = (dispatch) => {
  return ({
    'setMessage': message => dispatch(setIndicatorGroupMessage(message)),
    'setOpen': open => dispatch(setIndicatorGroupOpen(open)),
    'setCurrentBatchId': currentBatchId => dispatch(setIndicatorGroupCurrentBatchId(currentBatchId))
  });
}

const VisibleExecuteRowButton = connect(mapStateToProps, mapDispatchToProps)(ExecuteRowButton);

export default function createExecuteRowButton(button, recordId) {
  return <VisibleExecuteRowButton
    key={`execute_${recordId}`}
    parameter={button.parameter}
    recordId={recordId}>
  </VisibleExecuteRowButton>;
}
