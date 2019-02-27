import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import { isSidebarOpen } from './../../actions/sidebar';

import CssBaseline from '@material-ui/core/CssBaseline';
import Content from './Content';
import { MessageBar } from './MessageBar';
import { setMessageBarOpen } from '../../actions/messageBar';
import { AppBarView } from './AppBar/AppBarView';
import { DrawerView } from './Drawer/DrawerView';

class BaseDataView extends React.Component {
  setDrawerOpen = (setOpen) => {
    this.props.setSidebarOpen(setOpen);
  }
  render() {
    const { classes } = this.props;

    return (
      <React.Fragment>
        <CssBaseline />
        <div className={classes.root}>
          <AppBarView classes={classes} sidebarIsOpen={this.props.sidebarIsOpen} setDrawerOpen={this.setDrawerOpen}/>
          <DrawerView classes={classes} sidebarIsOpen={this.props.sidebarIsOpen} setDrawerOpen={this.setDrawerOpen}/>
          <main className={classes.content}>
            <Content />
          </main>
        </div>
        <MessageBar
          message={this.props.messageBarMessage}
          isOpen={this.props.messageBarIsOpen}
          setOpen={this.props.setMessageBarOpen}
        />
      </React.Fragment>
    );
  }
}

/*
 * BaseDataView.propTypes = {
 *   content: PropTypes.object.isRequired,
 * };
 */

const mapStateToProps = (state) => ({
  'sidebarIsOpen': state.sidebarIsOpen,
  'messageBarMessage': state.messageBarMessage,
});

const mapDispatchToProps = (dispatch) => ({
  'setSidebarOpen': (sidebarOpenState) => dispatch(isSidebarOpen(sidebarOpenState)),
  'setMessageBarOpen': (open) => dispatch(setMessageBarOpen(open)),
});

export default withStyles(styles)(withRouter(connect(mapStateToProps, mapDispatchToProps)(BaseDataView)));
