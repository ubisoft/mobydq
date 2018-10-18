import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { styles } from './../../styles/baseStyles';
import { withStyles } from '@material-ui/core/styles';
import { isOpen } from './../../actions/sidebar';

import classNames from 'classnames';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import Badge from '@material-ui/core/Badge';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import NotificationsIcon from '@material-ui/icons/Notifications';
import Typography from '@material-ui/core/Typography';

import { mainListItems } from '../../listItems';
import Content from './Content';

class BaseDataView extends React.Component {
  handleDrawerOpen() {
    this.props.isOpen(true);
  }

  handleDrawerClose() {
    this.props.isOpen(false);
  }

  render() {
    const { classes } = this.props;

    return (
      <React.Fragment>
        <CssBaseline />
        <div className={classes.root}>
          <AppBar
            position="absolute"
            className={classNames(classes.appBar, this.props.open && classes.appBarShift)}
          >
            <Toolbar disableGutters={!this.props.open} className={classes.toolbar}>
              <IconButton
                color="inherit"
                aria-label="Open drawer"
                onClick={this.handleDrawerOpen.bind(this)}
                className={classNames(
                  classes.menuButton,
                  this.props.open && classes.menuButtonHidden,
                )}
              >
                <MenuIcon />
              </IconButton>
              <Typography variant="title" color="inherit" noWrap className={classes.title}>
                Dashboard
              </Typography>
              <IconButton color="inherit">
                <Badge badgeContent={4} color="secondary">
                  <NotificationsIcon />
                </Badge>
              </IconButton>
            </Toolbar>
          </AppBar>
          <Drawer
            variant="permanent"
            classes={{
              'paper': classNames(classes.drawerPaper, !this.props.open && classes.drawerPaperClose)
            }}
            open={this.props.open}
          >
            <div className={classes.toolbarIcon}>
              <IconButton onClick={this.handleDrawerClose.bind(this)}>
                <ChevronLeftIcon />
              </IconButton>
            </div>
            <Divider />
            <List>{mainListItems}</List>
          </Drawer>
          <main className={classes.content}>
            <Content />
          </main>
        </div>
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
  'open': state.sidebarIsOpen
});

const mapDispatchToProps = (dispatch) => ({
  'isOpen': (sidebarOpenState) => dispatch(isOpen(sidebarOpenState))
});

export default withStyles(styles)(withRouter(connect(mapStateToProps, mapDispatchToProps)(BaseDataView)));
