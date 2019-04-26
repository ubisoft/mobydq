import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

import { setAlertDialog } from '../../actions/app';

class AlertDialog extends React.Component {
  setDialog = (dialog) => {
    this.props.setAlertDialog(dialog);
  };

  render() {
    const { alertDialog } = this.props;
    return (
      alertDialog !== null && <div>
        <Dialog
          open={alertDialog !== null}
          onClose={() => this.setDialog(null)}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{alertDialog.title}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              {alertDialog.description}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button color="primary" onClick={() => {
              alertDialog.onNo();
              this.setDialog(null);
            } } >
              {alertDialog.noText}
            </Button>
            <Button color="primary" autoFocus onClick={() => {
              alertDialog.onYes();
              this.setDialog(null);
            } }>
              {alertDialog.yesText}
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  'alertDialog': state.alertDialog
});

const mapDispatchToProps = (dispatch) => ({
  'setAlertDialog': (alertDialog) => dispatch(setAlertDialog(alertDialog))
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(AlertDialog));
