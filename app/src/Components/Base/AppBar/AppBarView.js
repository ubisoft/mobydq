import AppBar from '@material-ui/core/AppBar/AppBar';
import Toolbar from '@material-ui/core/Toolbar/Toolbar';
import NotificationsIcon from '@material-ui/icons/Notifications';
import IconButton from '@material-ui/core/IconButton/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Typography from '@material-ui/core/Typography/Typography';
import Badge from '@material-ui/core/Badge/Badge';
import React from 'react';
import classNames from 'classnames';

export const AppBarView = ({ classes, sidebarIsOpen, setDrawerOpen }) => <AppBar
  position="absolute"
  className={classNames(classes.appBar, sidebarIsOpen && classes.appBarShift)}
>
  <Toolbar disableGutters={!sidebarIsOpen} className={classes.toolbar}>
    <IconButton
      color="inherit"
      aria-label="Open drawer"
      onClick={() => setDrawerOpen(true)}
      className={classNames(
        classes.menuButton,
        'sidebarExpand',
        sidebarIsOpen && classes.menuButtonHidden,
      )}
    >
      <MenuIcon />
    </IconButton>
    <Typography variant="title" color="inherit" noWrap className={classes.title}>
      MobyDQ
    </Typography>
    <IconButton color="inherit">
      <Badge badgeContent={4} color="secondary">
        <NotificationsIcon />
      </Badge>
    </IconButton>
  </Toolbar>
</AppBar>;
