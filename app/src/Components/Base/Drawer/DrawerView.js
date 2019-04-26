import Drawer from '@material-ui/core/Drawer/Drawer';
import IconButton from '@material-ui/core/IconButton/IconButton';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import Divider from '@material-ui/core/Divider/Divider';
import List from '@material-ui/core/List/List';
import { mainListItems } from '../../../listItems';
import React from 'react';

import classNames from 'classnames';

export const DrawerView = ({ classes, sidebarIsOpen, setDrawerOpen }) => <Drawer
  variant="permanent"
  classes={{
    'paper': classNames(classes.drawerPaper, !sidebarIsOpen && classes.drawerPaperClose)
  }}
  open={sidebarIsOpen}
>
  <div className={classes.toolbarIcon}>
    <IconButton onClick={() => setDrawerOpen(false)}>
      <ChevronLeftIcon />
    </IconButton>
  </div>
  <Divider />
  <List>{mainListItems}</List>
</Drawer>;
