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
import AlertDialog from './AlertDialog';

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
          <AppBar
            position="absolute"
            className={classNames(classes.appBar, this.props.sidebarIsOpen && classes.appBarShift)}
          >
            <Toolbar disableGutters={!this.props.sidebarIsOpen} className={classes.toolbar}>
              <IconButton
                color="inherit"
                aria-label="Open drawer"
                onClick={() => this.setDrawerOpen(true)}
                className={classNames(
                  classes.menuButton,
                  'sidebarExpand',
                  this.props.sidebarIsOpen && classes.menuButtonHidden,
                )}
              >
                <MenuIcon />
              </IconButton>
              <Typography variant="title" color="inherit" noWrap className={classes.title}>
                MobyDQ
              </Typography>
              {/*
              Removed bell icon because it wasn't used yet
              <IconButton color="inherit">
                <Badge badgeContent={4} color="secondary">
                  <NotificationsIcon />
                </Badge>
              </IconButton>
              */}
            </Toolbar>
          </AppBar>
          <Drawer
            variant="permanent"
            classes={{
              'paper': classNames(classes.drawerPaper, !this.props.sidebarIsOpen && classes.drawerPaperClose)
            }}
            open={this.props.sidebarIsOpen}
          >
            <div className={classes.toolbarIcon}>
              <IconButton onClick={() => this.setDrawerOpen(false)}>
                <ChevronLeftIcon />
              </IconButton>
            </div>
            <Divider />
            <List>{mainListItems}</List>
          </Drawer>
          <DrawerView classes={classes} sidebarIsOpen={this.props.sidebarIsOpen} setDrawerOpen={this.setDrawerOpen}/>
          <AlertDialog/>
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
  'messageBarMessage': state.messageBarMessage
});

const mapDispatchToProps = (dispatch) => ({
  'setSidebarOpen': (sidebarOpenState) => dispatch(isSidebarOpen(sidebarOpenState)),
  'setMessageBarOpen': (open) => dispatch(setMessageBarOpen(open))
});

export default withStyles(styles)(withRouter(connect(mapStateToProps, mapDispatchToProps)(BaseDataView)));
