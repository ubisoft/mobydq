import React from 'react';
import { Link } from 'react-router-dom';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DashboardIcon from '@material-ui/icons/ViewQuilt';
import IndicatorIcon from '@material-ui/icons/Timeline';
import IndicatorGroupIcon from '@material-ui/icons/Folder';
import DataSourceIcon from '@material-ui/icons/Cloud';
import AdminIcon from '@material-ui/icons/Settings';
import LoginOutDrawerItem from './Components/Login/LoginOutDrawerItem';
import UserGroupIcon from '@material-ui/icons/Group';
import UserIcon from '@material-ui/icons/Person';

export const mainListItems =
  <div>
    <ListItem button component={Link} to="/">
      <ListItemIcon>
        <DashboardIcon/>
      </ListItemIcon>
      <ListItemText primary="Dashboard"/>
    </ListItem>
    <ListItem button component={Link} to="/indicator">
      <ListItemIcon>
        <IndicatorIcon/>
      </ListItemIcon>
      <ListItemText primary="Indicators"/>
    </ListItem>
    <ListItem button component={Link} to="/indicator-group">
      <ListItemIcon>
        <IndicatorGroupIcon/>
      </ListItemIcon>
      <ListItemText primary="Indicator Groups"/>
    </ListItem>
    <ListItem button component={Link} to="/data-source">
      <ListItemIcon>
        <DataSourceIcon/>
      </ListItemIcon>
      <ListItemText primary="Data Sources"/>
    </ListItem>
    <ListItem button component={Link} to="/user-group">
      <ListItemIcon>
        <UserGroupIcon />
      </ListItemIcon>
      <ListItemText primary="User Groups" />
    </ListItem>
    <ListItem button component={Link} to="/user">
      <ListItemIcon>
        <UserIcon />
      </ListItemIcon>
      <ListItemText primary="Users" />
    </ListItem>
    <ListItem button component={Link} to="/admin">
      <ListItemIcon>
        <AdminIcon/>
      </ListItemIcon>
      <ListItemText primary="Admin"/>
    </ListItem>
    <LoginOutDrawerItem/>
  </div>;
