import React from 'react';
import { Link } from 'react-router-dom'
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import DashboardIcon from '@material-ui/icons/ViewQuilt';
import IndicatorIcon from '@material-ui/icons/Timeline';
import IndicatorGroupIcon from '@material-ui/icons/Folder';
import DataSourceIcon from '@material-ui/icons/Cloud';
import AdminIcon from '@material-ui/icons/Settings';

export const mainListItems = (
  <div>
    <ListItem button component={Link} to="/">
      <ListItemIcon>
        <DashboardIcon />
      </ListItemIcon>
      <ListItemText primary="Dashboard" />
    </ListItem>
      <ListItem button component={Link} to="/indicator">
      <ListItemIcon>
        <IndicatorIcon />
      </ListItemIcon>
      <ListItemText primary="Indicators" />
    </ListItem>
    <ListItem button component={Link} to="/indicator-group">
      <ListItemIcon>
        <IndicatorGroupIcon />
      </ListItemIcon>
      <ListItemText primary="Indicator Groups" />
    </ListItem>
    <ListItem button component={Link} to="/data-source">
      <ListItemIcon>
        <DataSourceIcon />
      </ListItemIcon>
      <ListItemText primary="Data Sources" />
    </ListItem>
    <ListItem button component={Link} to="/admin">
      <ListItemIcon>
        <AdminIcon />
      </ListItemIcon>
      <ListItemText primary="Admin" />
    </ListItem>
  </div>
);